 🤖 JARVIS-2025 — AI Personal Assistant (Powered by LLMs + Voice + Automation)

JARVIS-2025 is a real-time AI assistant designed to run locally on your laptop.
It supports voice commands, face authentication, web automation, 
device control, conversation memory, and **AI reasoning** using local & cloud LLMs.

This is my final-year project for B.Tech (AI & Data Science).

---

 🚀 Features

 🎙️ **Voice Interaction**
- Wake-word support
- Real-time speech-to-text
- Natural AI conversation (OpenAI / Ollama / GPT)

🧑‍🦰 **Face Authentication**
- Login to JARVIS using face recognition
- Prevent unauthorized access

### 🌐 **Web & App Automation**
- Open apps (Chrome, YouTube, WhatsApp, VS Code, etc.)
- Search Google
- Send WhatsApp messages
- System control (volume, battery status, shutdown, etc.)

### 🧠 **Advanced AI Abilities**
- Local LLM support using **Ollama**
- Memory-based conversation
- Code generation help
- Document reading and summarization

### 🏠 **Smart Home Automation (Optional)**
- Control IoT devices
- Connect with ESP32 / NodeMCU

### 💾 **Database**
- SQLite (jarvis.db) for storing:
  - Chat logs
  - User profiles
  - System settings

---

## 📂 Project Structure

Jarvis-2025/
│
├── backend/
│ ├── ai_engine/ # AI processing
│ ├── audio/ # STT & TTS files
│ ├── automation/ # Web / system automation
│ └── database/ # jarvis.db functions
│
├── frontend/
│ ├── ui/ # GUI files (Tkinter / React etc.)
│
├── envJarvis/ # Virtual environment (ignored)
├── main.py # Start JARVIS
├── run.py # Frontend + backend launcher
├── ollama_backend.py # Local LLM integration
├── README.md # Project documentation
└── .gitignore

yaml
Copy code

---

## 🛠️ Tech Stack

### **AI / ML**
- Python
- OpenAI GPT / Local LLMs (Ollama, Llama 3)
- SpeechRecognition
- Face Recognition (dlib / cv2)
- Pyttsx3 / gTTS

### **Backend**
- FastAPI / Flask (optional)
- SQLite database
- Automation via PyAutoGUI, Selenium

### **Frontend**
- Tkinter / React (based on your project preference)

---

## ⚙️ Installation Guide

### **1. Clone the Repository**
git clone https://github.com/harshalcoder-ai/JARVIS-2025.git
cd JARVIS-2025

markdown
Copy code

### **2. Create Virtual Environment**
python -m venv envJarvis
envJarvis\Scripts\activate

markdown
Copy code

### **3. Install Requirements**
pip install -r requirements.txt

csharp
Copy code

### **4. Install Ollama (for local LLM)**
Download from: https://ollama.ai

Then run:
ollama pull llama3

markdown
Copy code

### **5. Run JARVIS**
python main.py

yaml
Copy code

---

## 🎯 Usage Examples

### **Speak:**
- "Jarvis, open YouTube"
- "Send a message to Rahul"
- "Explain binary search"
- "Give me today's weather"
- "Play music"

### **Keyboard run:**
python run.py

yaml
Copy code

---

## 🎥 Screenshots / Demo (Add Your Images)

📸 Coming soon…

yaml
Copy code

(You can add .png images in a `screenshots/` folder)

---

## 🛣️ Future Improvements (Roadmap)

- Add GPT-4o mini vision support
- Add Rasa for improved conversational flow
- Add personal calendar/schedule planner
- Make Android app to control JARVIS
- Add home automation dashboard
- Add continuous listening mode
- Add multi-user voice profile recognition

---

## 🤝 Contribution

If you want to improve the project:
Fork → Modify → Pull Request

yaml
Copy code

---

## 📄 License
MIT License

---

## 👨‍💻 Author
**Harshal Sonkusare**  
B.Tech – Artificial Intelligence & Data Science  
GitHub: https://github.com/harshalcoder-ai  
Email: harshalsonkisare@gmail.com  

---

## ⭐ Support This Project
If you like this project, please give it a ⭐ on GitHub! 😊
