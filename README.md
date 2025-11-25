# 🏫 Bennett Info Bot

A smart desktop assistant for **Bennett University**, built using **Python + Tkinter + Gemini API**. This application helps students and visitors navigate the campus, find facilities, and get accurate university-related information using AI combined with a structured private knowledge system.

---

## ✨ Features

### 🤖 AI-Powered University Assistant

* Uses **Google Gemini API** for natural language understanding.
* Strictly answers only Bennett University-related queries.
* Provides clear, contextual, and student-friendly responses.

### 🗺 Campus Map Panel

* Displays a campus map alongside the chat interface.
* Supports custom map image (`campus_map.png`).
* Useful for orientation and quick visual reference.

### 🧭 Direction-Based Responses

* Generates step-by-step navigation such as:

  > From A Block, walk straight and turn left to reach Snapeats.

### 🧠 Private Knowledge Base

* Uses `private_data.json` as a trusted internal data source.
* Ensures high accuracy for locations, buildings, and facilities.

### 🎨 Modern UI (Tkinter)

* Light / Dark mode toggle
* Clear Chat button
* Animated "Thinking..." indicator
* Clean, responsive chat layout

---

## 🛠 Tech Stack

| Component  | Technology        |
| ---------- | ----------------- |
| Frontend   | Tkinter           |
| AI Engine  | Google Gemini API |
| Data Store | JSON              |
| Language   | Python 3.x        |

---

## 📂 Project Structure

```
bennett-info-bot/
│
├── main.py             # Application entry point
├── ui.py               # Tkinter UI logic
├── api_client.py       # Gemini API communication
├── config.py           # Configuration & system prompt
├── private_data.json   # Internal structured knowledge
├── campus_map.png      # Optional campus map image
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/nolifer-acey/bennett_chatbot.git
cd bennett_chatbot
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set your Gemini API Key

Linux / Mac:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Windows (PowerShell):

```powershell
setx GEMINI_API_KEY "YOUR_API_KEY"
```

### 4️⃣ Run the application

```bash
python main.py
```

---

## 🧭 Example Queries

* "Where is Gobble?"
* "How to go from A block to German Hanger"
* "What food outlets are in N block?"
* "What sports facilities does Bennett have?"

---

## 🔮 Future Enhancements

### 🗺 Interactive Map System

* Clickable buildings
* Highlighted navigation paths
* Zoom & Pan controls
* Real-time position tracking

### 📍 Smart Navigation

* Shortest path algorithm
* Route optimization
* Indoor positioning

### 🎤 Voice Assistant Mode

* Speech-to-text input
* Text-to-speech output
* Hands-free interaction

### 📱 Mobile Expansion

* Android version (Kivy / Flutter)
* QR-based campus locators

### 🧠 AI Memory

* Personalized preferences
* Hostel-aware suggestions
* Frequently visited places

### 🏢 Multi-Mode Assistant

* Admissions Mode
* Academic Mode
* Placement Mode
* Hostel Mode

### 🔔 Notification System

* Event alerts
* Timetable reminders
* Library due-date notices

### 🎓 Student Portal Integration

* Bennett ID login
* Attendance & timetable view
* Academic progress tracking

### 📊 Analytics Dashboard

* Popular queries
* Heatmap of campus movement
* Usage insights

### 🌐 Multi-Language Support

* Hindi
* Bengali
* Regional languages

---

## 🌟 Vision

This project aims to evolve into a **Smart Campus Ecosystem**, assisting with:

* First-year navigation
* Visitor guidance
* Emergency route assistance
* Personalized campus experiences
* Intelligent academic planning

---

## 🙌 Contributing

Contributions are welcome! You can help by:

* Enhancing the UI
* Improving AI prompt logic
* Optimizing performance
* Expanding map and navigation features

Fork the repository and submit a pull request 🚀

---

## 📜 License

This project is intended for educational and campus-support use. Feel free to modify and extend it with proper attribution.

---

### 💡 Developed for Bennett University Students & Visitors

Making campus navigation smarter, faster, and friendlier.
