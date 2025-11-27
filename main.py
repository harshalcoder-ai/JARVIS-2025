import os
import eel
import subprocess
from backend.auth import recoganize
from backend.auth.recoganize import AuthenticateFace
from backend.feature import *
from backend.command import *

import pyttsx3  # For text-to-speech

# ----------------- Initialize TTS -----------------
engine = pyttsx3.init()

def speak(text):
    """
    Speak the given text aloud.
    """
    engine.say(text)
    engine.runAndWait()

# ----------------- Ollama Integration -----------------
def ask_ollama(prompt):
    """
    Sends a question to Ollama CLI and returns the answer as text.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1-8b", "--prompt", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------- Main Function -----------------
def start():
    # Initialize frontend folder
    eel.init("frontend")

    play_assistant_sound()

    # Expose function to JS
    @eel.expose
    def init():
        eel.hideLoader()
        speak("Welcome to Jarvis")
        speak("Ready for Face Authentication")

        flag = recoganize.AuthenticateFace()
        if flag == 1:
            speak("Face recognized successfully")
            eel.hideFaceAuth()
            eel.hideFaceAuthSuccess()
            speak("Welcome to Your Assistant")
            eel.hideStart()
            play_assistant_sound()
        else:
            speak("Face not recognized. Please try again")

    # ----------------- New: Ask Ollama from frontend -----------------
    @eel.expose
    def askJarvis(question):
        """
        Receives question from frontend JS and returns answer from Ollama.
        """
        speak("Processing your question...")
        answer = ask_ollama(question)  # Call Ollama CLI
        speak(answer)
        return answer

    # Start frontend (single call only!)
    eel.start("index.html", mode="default", size=(1000, 600))


# ----------------- Run the assistant -----------------
if __name__ == "__main__":
    start()
