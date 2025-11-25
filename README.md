# 🏫 Bennett Info Bot

An intelligent desktop assistant for **Bennett University**, built with **Python + Tkinter + Gemini API**. This bot helps students navigate the campus, find locations, explore facilities, and get accurate university-related information using a combination of AI and a structured private knowledge base.

---

## ✨ Features

### 🤖 Smart AI Assistant

* Powered by **Google Gemini API** for natural language understanding.
* Restricts answers strictly to Bennett University–related queries.
* Gives clear, contextual, and student-friendly responses.

### 🗺 Visual Campus Map Panel

* Displays a live campus map alongside the chat.
* Supports custom uploaded map image (`campus_map.png`).
* Perfect for navigation and orientation.

### 🧭 Direction-Based Answers

* Step-by-step navigation like:

  > From A Block, walk straight and turn left to reach Snapeats.

### 🧠 Private Knowledge System

* Uses `private_data.json` as a trusted internal source.
* Ensures campus locations and facilities are always accurate.

### 🎨 Modern Tkinter UI

* Light/Dark Mode toggle
* Clear Chat button
* Animated "Thinking..." response
* Side-by-side Chat + Map layout

---

## 🛠 Tech Stack

| Component      | Technology        |
| -------------- | ----------------- |
| Frontend       | Tkinter           |
| AI Engine      | Google Gemini API |
| Data Storage   | JSON              |
| Language       | Python 3.x        |

---

## 📂 Project Structure

```
bennett-info-bot/
│
├── bennett_tk_bot.py        # Main application
├── private_data.json        # Internal structured knowledge
├── README.md                # Documentation
└── requirements.txt         # Dependencies
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/bennett-info-bot.git
cd bennett-info-bot
```

### 2. Set your Gemini API Key

Linux / Mac:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Windows (PowerShell):

```powershell
setx GEMINI_API_KEY "YOUR_API_KEY"
```

### 3. Run the app

```bash
python main.py
```

---

## 🧭 Usage Examples

* "Where is Gobble?"
* "How to go from A block to German Hanger"
* "What food outlets are in N block?"
* "What sports facilities does Bennett have?"

---

# 🔮 Future Scope & Enhancements

Here are the potential next-generation upgrades for your bot 🚀

## 1. 🗺 Interactive Map System

* Clickable buildings
* Highlight path from source to destination
* Zoom & Pan controls
* Real-time position tracking

## 2. 📍 Smart Navigation

* "Navigate me from C11 to LRC"
* Shortest route algorithm
* Indoor GPS support (future IoT integration)

## 3. 🎤 Voice Assistant Mode

* Speech-to-text queries
* Text-to-speech responses
* Hands-free navigation

## 4. 📱 Mobile App Version

* Android version using Kivy or Flutter
* QR-based campus scanners

## 5. 🧠 AI Memory System

* Personalized student profiles
* Hostel-aware suggestions
* Favorite places memory

## 6. 🏢 Department-Specific Bot

* Different modes for:

  * Admissions
  * Academics
  * Placements
  * Hostels

## 7. 🔔 Notification System

* Timetable reminders
* Event alerts
* Library due-date warnings

## 8. 🎓 Student Portal Integration

* Login with Bennett ID
* Course & timetable display
* Attendance tracking

## 9. 📊 Analytics Dashboard

* Most searched locations
* Popular queries
* Student movement heatmap

## 10. Multi-Language Support

* Hindi
* Bengali
* Regional language support

---

## 🌟 Vision

This project can evolve into a **full-scale Smart Campus Assistant**, supporting:

* First-year navigation
* Visitor guidance
* Emergency directions
* Real-time event info
* Personalized academic planning

---

## 🙌 Contributing

Pull requests are welcome!

Future contributors can help with:

* UI enhancements
* AI prompt engineering
* Map system improvements
* Performance optimization

---

## 📜 License

This project is intended for educational and campus assistance use.
You may adapt or extend it with proper attribution.

---

## 👨‍💻 Author

Developed by **Souhard Roy**
B.Tech CSE Student, Bennett University

---
