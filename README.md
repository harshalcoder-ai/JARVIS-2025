🤖 JARVIS-2025 — AI Personal Assistant 

A Fully Intelligent, Offline + Online Hybrid AI Assistant with Voice, Vision, Automation, Reasoning, Memory & App Control

🧭 Table of Contents

Project Overview
Key Capabilities
System Architecture
Technology Stack
Installation (Very Detailed)
Configuration & Environment Setup
Project Folder Structure
How It Works (Internal Pipeline Explained)
Usage Examples
API Documentation (Internal Functions)
Local LLM Support via Ollama
Database Schema
Screenshots & Demo Videos
Troubleshooting Guide
Roadmap
Author


🧠 Project Overview

JARVIS-2025 is an advanced AI personal assistant that runs locally on your system and can also connect to cloud LLMs.
This assistant can:
Listen, speak, and reason
Automate tasks
Control your apps
Understand your voice
Identify your face
Remember previous conversations
Execute commands like a real JARVIS

This project is developed as a final-year engineering project (AI & Data Science), but designed to work like a production-level personal AI system.


🚀 Key Capabilities
🎙️ 1. Voice Processing
Real-time speech-to-text
Natural AI voice responses
Wake-word activation (optional)

🧑‍🦰 2. Face Authentication
Uses OpenCV + Dlib
Locks/unlocks the assistant
Multi-user support (optional)

🤖 3. AI Reasoning
Supports:
GPT-4o
GPT-4o-mini
Llama 3 (via Ollama)
Mistral
Phi 3

💻 4. System Automation
Open apps
Close apps
Control system volume
Play music
Capture screenshots
Create notes

🌐 5. Web Automation
Google search
YouTube search
WhatsApp automation
Email automation

🧾 6. Database Support
Stores:
Chat history
Settings
User profiles
Face embeddings


🏗️ System Architecture
                    ┌──────────────────────────┐
                    │   Microphone Input        │
                    └─────────────┬────────────┘
                                  │
                        Speech-to-Text (STT)
                                  │
                    ┌─────────────▼────────────┐
                    │ Natural Language Engine   │
                    │  (OpenAI/Ollama/GPT)      │
                    └─────────────┬────────────┘
                                  │
                         Intent Classification
                                  │
          ┌───────────────────────┼──────────────────────────┐
          │                       │                          │
   System Automation        Knowledge Query              Face/Voice Tasks
(PyAutoGUI / OS / APIs)     (LLM/Database)              (OpenCV / Dlib)
          │                       │                          │
          └───────────────┬───────┴────────────┬────────────┘
                          │                    │
                        Response Generator (TTS)
                          │
                          ▼
                    Speaker Output



🛠️ Technology Stack
Languages
Python
JavaScript (optional for frontend)

AI Libraries
OpenAI API
Ollama (local LLM)
Langchain (if using)
SpeechRecognition
Pyttsx3 / Edge-TTS

Vision
OpenCV
Dlib
Face Recognition library

Backend
Python
FastAPI / Flask (optional)

Database
SQLite3 (jarvis.db)

Automation
PyAutoGUI
Selenium
OS module

📦 Installation (Very Detailed)
🔹 Step 1 — Clone the Repository
git clone https://github.com/harshalcoder-ai/JARVIS-2025.git
cd JARVIS-2025

🔹 Step 2 — Create Virtual Environment
python -m venv envJarvis


Activate:
envJarvis\Scripts\activate

🔹 Step 3 — Install Dependencies
pip install -r requirements.txt


If missing, install manually:
pip install openai speechrecognition pyttsx3 opencv-python dlib pyautogui

🔹 Step 4 — Setup Ollama (Local LLM)
Download Ollama → https://ollama.ai

Then:
ollama pull llama3

🔹 Step 5 — Run the Assistant
python main.py

⚙️ Configuration & Environment Setup
In config.json:

{
  "openai_api_key": "YOUR_KEY",
  "use_ollama": true,
  "model": "gpt-4o-mini",
  "wake_word": "jarvis"
}


📁 Project Folder Structure
Jarvis-2025/
│
├── backend/
│   ├── stt/            # Speech to text
│   ├── tts/            # Text to speech
│   ├── ai_engine/      # OpenAI/Ollama logic
│   ├── automation/     # OS & web automation modules
│   ├── vision/         # Face recognition, camera
│   ├── database/       # SQLite database wrapper
│   └── utils/          # Helper functions
│
├── frontend/           # Optional UI (React/Tkinter)
│
├── envJarvis/          # Virtual env (not pushed to GitHub)
│
├── main.py             # Entry point
├── run.py              # Starts frontend + backend
├── README.md
├── .gitignore
└── jarvis.db

🧠 How It Works (Internal Pipeline Explained)
1. Wake Word Detection
Continuously listens for “Jarvis”
Low CPU consumption

2. Speech Recognition
Converts your voice to text
Removes background noise

3. Intent Understanding
Uses LLM to classify:
System command
Automation task
Question-answering
Face-related task
Web automation

5. Execution Layer
Uses:
pyautogui → Click, type, scroll
selenium → automate web
os → open/close apps

5. Response Generation
The assistant speaks the answer using TTS.

💬 Usage Examples
**Speak:**
- "Jarvis, open YouTube"
- "Send a message to Rahul"
- "Explain binary search"
- "Give me today's weather"
- "Play music"


📘 API Documentation (Internal Functions)
Example:
backend/automation/system.py
def open_application(app_name):
    """
    Opens an application by name.
    Supported: chrome, vs code, notepad, camera.
    """

backend/ai_engine/engine.py
def ask_ai(query):
    """
    Handles both OpenAI GPT and Ollama.
    Returns LLM response as text.
    """

backend/voice/stt.py
def listen_to_user():
    """
    Converts microphone audio into text using SpeechRecognition.
    """

🗄️ Database Schema
TABLE history (
    id INTEGER PRIMARY KEY,
    user_input TEXT,
    ai_response TEXT,
    timestamp DATETIME
);

TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    face_encoding BLOB
);

🧩 Troubleshooting Guide
Issue	                        Reason	                                    Fix
Microphone not working	     STT error	                           Check input device
Dlib error                	Missing C++ build tools             	Install vs_buildtools.exe
Model not responding       	Wrong OpenAI key               	      Add a valid API key
“No module found”	      Virtual environment not activated	     Run envJarvis\Scripts\activate


🚀 Roadmap
 Add real-time animated UI
 Add multi-user authentication
 Full mobile app
 Add offline vision-language model
 Smart home dashboard

👨‍💻 Author
Harshal Sonkusare
B.Tech Artificial Intelligence & Data Science
Email: harshalsonkisare@gmail.com
GitHub: https://github.com/harshalcoder-ai

⭐ Support

If this project helps you, please ⭐ the repo!
