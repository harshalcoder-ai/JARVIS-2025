:

🤖 JARVIS-2025 — AI Desktop Assistant

Advanced voice-controlled AI assistant with system automation, face authentication, and local LLM support.

🚀 Features

🔐 Face Authentication (OpenCV + LBPH)

🎙️ Voice Recognition (SpeechRecognition)

🧠 Offline AI Chat using Ollama

⚙️ System Command Automation

🌐 Open Websites & Applications

🗂️ SQLite Database Support

💬 Frontend Dashboard with Animations

🔈 Text-to-Speech Responses

📁 Modular Backend Architecture

📸 Image-based detection modules (optional)

🧰 Tech Stack
Languages

Python

JavaScript

HTML/CSS

Libraries

OpenCV

Pyttsx3

SpeechRecognition

SQLite3

Requests

PyAutoGUI

Subprocess

Ollama API

Tools

VS Code

Git & GitHub

Python Virtual Environment

📁 Project Structure
Jarvis-2025/
│── backend/
│   ├── auth/            → Face authentication
│   ├── command.py       → System commands
│   ├── feature.py       → Main features
│   ├── db.py            → Database operations
│   ├── helper.py        → Utility functions
│   ├── apis.py          → External APIs
│   └── open_command.py  → Website & app shortcuts
│
│── frontend/
│   ├── index.html
│   ├── main.js
│   ├── style.css
│   └── assets/
│
│── ollama_backend.py
│── run.py
│── main.py
│── README.md
│── .gitignore

🛠️ Installation
1️⃣ Clone the repository
git clone https://github.com/harshalcoder-ai/JARVIS-2025.git
cd JARVIS-2025

2️⃣ Create virtual environment
python -m venv envJarvis
envJarvis\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the assistant
python run.py

🎙️ How to Use

Start JARVIS

Face authentication will verify user

Say your command (examples):

"Jarvis open YouTube"

"Play music"

"Tell me the time"

"Search on Google"

"Explain Python classes" (LLM)

JARVIS speaks and executes tasks in real-time

🔮 Future Improvements

GPT-4o Realtime API integration

Hand gesture control

Offline STT + TTS

Android mobile app extension

Home automation integration

Browser-level automation

👨‍💻 Author

Harshal Sonkusare
B.Tech Final Year — Artificial Intelligence & Data Science
Email: harshalsonkisare@gmail.com

GitHub: https://github.com/harshalcoder-ai
