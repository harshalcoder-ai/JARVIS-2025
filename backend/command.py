import time
import pyttsx3
import speech_recognition as sr
import eel

# =====================================================
# 🎛️ GLOBAL MODE (Voice/Text)
# =====================================================
assistant_mode = "voice"  # default mode


def set_mode(new_mode):
    """
    Switch between 'voice' and 'text' mode.
    """
    global assistant_mode
    if new_mode in ["voice", "text"]:
        assistant_mode = new_mode
        speak(f"Switched to {new_mode} mode.")
        print(f"[Mode]: {assistant_mode}")
        return f"Mode changed to {new_mode}"
    else:
        speak("Invalid mode.")
        return "Invalid mode"


def get_mode():
    """
    Returns current mode (voice or text).
    """
    return assistant_mode


# =====================================================
# 🔊 SPEAK FUNCTION
# =====================================================
def speak(text):
    """
    Speaks and sends text to frontend.
    Only speaks if in voice mode.
    """
    text = str(text)
    eel.DisplayMessage(text)
    eel.receiverText(text)
    print(f"Jarvis: {text}")

    if assistant_mode == "voice":
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[2].id if len(voices) > 2 else voices[0].id)
            engine.setProperty('rate', 174)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[Speak ERROR]: {e}")


# =====================================================
# 🎙️ LISTEN FUNCTION
# =====================================================
def takecommand():
    """
    Listens for voice input and returns recognized text.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 I'm listening...")
        eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 8)

    try:
        print("🎤 Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        eel.senderText(query)
        return query.lower()
    except Exception as e:
        print(f"[Voice ERROR]: {e}")
        speak("Sorry, I didn’t catch that.")
        return None


# =====================================================
# ⚙️ COMMAND HANDLER
# =====================================================
@eel.expose
def takeAllCommands(message=None):
    """
    Handles both voice and text commands.
    """
    if message is None:
        query = takecommand()  # Voice input
        if not query:
            return
    else:
        query = message  # Text input
        print(f"Message received: {query}")
        eel.senderText(query)

    try:
        # =====================================================
        # 🧩 VOICE / TEXT MODE CONTROL
        # =====================================================
        if "text mode" in query:
            set_mode("text")
            return
        elif "voice mode" in query:
            set_mode("voice")
            return

        # =====================================================
        # 🌐 NORMAL COMMANDS
        # =====================================================
        if "open" in query:
            from backend.feature import openCommand
            openCommand(query)

        elif "send message" in query or "call" in query or "video call" in query:
            from backend.feature import findContact, whatsApp
            flag = ""
            Phone, name = findContact(query)
            if Phone != 0:
                if "send message" in query:
                    flag = 'message'
                    speak("What message should I send?")
                    msg = takecommand()
                elif "call" in query:
                    flag = 'call'
                    msg = ""
                else:
                    flag = 'video call'
                    msg = ""
                whatsApp(Phone, msg, flag, name)

        elif "on youtube" in query:
            from backend.feature import PlayYoutube
            PlayYoutube(query)

        else:
            from backend.feature import chatBot
            response = chatBot(query)
            if get_mode() == "text":
                eel.DisplayMessage(response)
            else:
                speak(response)

    except Exception as e:
        print(f"[Command ERROR]: {e}")
        speak("Sorry, something went wrong.")
    
    eel.ShowHood()
