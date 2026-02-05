import os
import eel
import subprocess
import pyttsx3

from backend.auth import recoganize
from backend.feature import *
from backend.command import *

# -------- SAFE IMPORTS FROM JARVIS_FEATURES --------
try:
    import JARVIS_FEATURES.memory_system as memory_module
    import JARVIS_FEATURES.multi_agent_swarm as swarm_module
    import JARVIS_FEATURES.computer_vision as vision_module
    import JARVIS_FEATURES.emotional_intelligence as emotion_module
except Exception as e:
    print("Error importing JARVIS_FEATURES:", e)
    memory_module = None
    swarm_module = None
    vision_module = None
    emotion_module = None


# ----------------- Initialize TTS -----------------
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


# ----------------- Ollama Integration -----------------
def ask_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1-8b", "--prompt", prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {str(e)}"


# ----------------- Initialize AI Systems Safely -----------------
memory = None
swarm = None

if memory_module and hasattr(memory_module, "MemorySystem"):
    memory = memory_module.MemorySystem()

if swarm_module and hasattr(swarm_module, "SwarmController"):
    swarm = swarm_module.SwarmController()


# ----------------- Main Function -----------------
def start():
    eel.init("frontend")
    play_assistant_sound()

    # -------- Face Authentication --------
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


    # -------- Ask Jarvis --------
    @eel.expose
    def askJarvis(question):
        speak("Processing your question...")

        detections = None
        emotion = "neutral"

        # ----- Computer Vision -----
        if vision_module and hasattr(vision_module, "get_camera_frame") and hasattr(vision_module, "detect_objects"):
            frame = vision_module.get_camera_frame()
            detections = vision_module.detect_objects(frame)

        # ----- Memory -----
        if memory and detections is not None:
            memory.store(detections)

        # ----- Swarm -----
        if swarm and detections is not None:
            swarm.update(detections)

        # ----- Emotion -----
        if emotion_module and hasattr(emotion_module, "analyze_scene") and detections is not None:
            emotion = emotion_module.analyze_scene(detections)

        print("AI Emotion:", emotion)

        # ----- LLM -----
        answer = ask_ollama(question)

        speak(answer)

        return f"{answer}\n\n[Emotion: {emotion}]"


    eel.start("index.html", mode="default", size=(1000, 600))


# ----------------- Run -----------------
if __name__ == "__main__":
    start()
