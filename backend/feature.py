# ----------------- Imports -----------------
import os
import re
import struct
import subprocess
import time
import webbrowser
import sqlite3

import eel
import pygame
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
from shlex import quote
import ollama  # ✅ Ollama for offline AI

from backend.command import speak
from backend.config import ASSISTANT_NAME
from backend.helper import extract_yt_term, remove_words
from backend.open_command import open_command_router
from backend.apis import (
    get_weather,
    get_news,
    get_wikipedia,
    get_stock,
    duckduck_search,
)

# ----------------- Database -----------------
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# ----------------- Audio Init -----------------
pygame.mixer.init()

# ----------------- Sound -----------------
@eel.expose
def play_assistant_sound():
    sound_file = os.path.join("frontend", "assets", "audio", "start_sound.mp3")
    if not os.path.exists(sound_file):
        print(f"[Warning] Sound file not found: {sound_file}")
        return
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()


# ----------------- Open Command -----------------
@eel.expose
def openCommand(query):
    """
    Wrapper for open commands. Routes to backend/open_command.py
    Returns a dict with status & action so Eel doesn’t KeyError.
    """
    try:
        result = open_command_router(query, speak_fn=speak)
        return result
    except Exception as e:
        print("[openCommand wrapper ERROR]:", e)
        speak("Sorry, I couldn't open that.")
        return {"status": False, "error": str(e)}


# ----------------- YouTube -----------------
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)


# ----------------- Hotword Activation -----------------
def hotword():
    porcupine, paud, audio_stream = None, None, None
    try:
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("[Hotword] Detected")
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")

    except Exception as e:
        print("[hotword ERROR]:", e)
    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()


# ----------------- Contacts -----------------
def findContact(query):
    words_to_remove = [
        ASSISTANT_NAME, "make", "a", "to", "phone", "call",
        "send", "message", "whatsapp", "video"
    ]
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        cursor.execute(
            "SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
            ('%' + query + '%', query + '%')
        )
        results = cursor.fetchall()
        if not results:
            raise ValueError("Contact not found")

        mobile_number = str(results[0][0])
        if not mobile_number.startswith("+91"):
            mobile_number = "+91" + mobile_number

        return mobile_number, query

    except Exception as e:
        print("[findContact ERROR]:", e)
        speak("Not found in contacts")
        return 0, 0


# ----------------- WhatsApp -----------------
def whatsApp(Phone, message, flag, name):
    if flag == "message":
        target_tab, jarvis_message = 12, f"Message sent successfully to {name}"
    elif flag == "call":
        target_tab, message, jarvis_message = 7, "", f"Calling {name}"
    else:
        target_tab, message, jarvis_message = 6, "", f"Starting video call with {name}"

    try:
        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"
        full_command = f'start "" "{whatsapp_url}"'

        subprocess.run(full_command, shell=True)
        time.sleep(5)
        subprocess.run(full_command, shell=True)

        pyautogui.hotkey("ctrl", "f")
        for _ in range(1, target_tab):
            pyautogui.hotkey("tab")
        pyautogui.hotkey("enter")

        speak(jarvis_message)

    except Exception as e:
        print("[whatsApp ERROR]:", e)
        speak("Something went wrong with WhatsApp")


# ----------------- Global Chat Memory -----------------
chat_memory = []


# ----------------- ChatBot (Memory + APIs + Ollama) -----------------
def chatBot(query: str):
    """
    Unified AI logic:
    - Keeps short chat memory for context
    - Handles weather, news, Wikipedia, search, stock queries
    - Falls back to Ollama (Llama3.1) for reasoning and conversation
    """
    global chat_memory
    query = query.strip()
    q = query.lower()

    # Save user message to memory
    chat_memory.append({"role": "user", "content": query})
    if len(chat_memory) > 6:
        chat_memory = chat_memory[-6:]

    # 🌦️ Weather
    if "weather" in q:
        city = q.replace("weather", "").replace("in", "").strip()
        if not city:
            city = "Nagpur"
        answer = get_weather(city)
        speak(answer)
        return answer

    # 📰 News
    if "news" in q or "headlines" in q:
        answer = get_news()
        speak(answer)
        return answer

    # 📚 Wikipedia
    if "who is" in q or "tell me about" in q:
        topic = q.replace("who is", "").replace("tell me about", "").strip()
        answer = get_wikipedia(topic)
        speak(answer)
        return answer

    # 🌍 Live Web Search
    if any(x in q for x in ["search", "find", "latest", "current", "today", "now", "information about"]):
        answer = duckduck_search(q)
        speak(answer)
        return answer

    # 💹 Stock Prices
    if "stock" in q or "share price" in q:
        symbol = q.split()[-1].upper()
        answer = get_stock(symbol)
        speak(answer)
        return answer

    # 🧠 Default → Ollama (Offline AI with memory)
    try:
        response = ollama.chat(
            model="llama3.1",
            messages=chat_memory
        )
        answer = response["message"]["content"]

        # Add assistant reply to memory
        chat_memory.append({"role": "assistant", "content": answer})

        print("[Ollama Response]:", answer)
        speak(answer)
        return answer

    except Exception as e:
        print("[Ollama ERROR]:", e)
        speak("Sorry, I couldn't process your request.")
        return "Error"
