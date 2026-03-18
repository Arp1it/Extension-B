# 🧠 Echo Voice Assistant (Blind Accessibility Project)

Echo is a real-time voice assistant designed to help visually impaired users interact with the web using only their voice.

It listens, understands, responds, and even opens websites — without requiring manual interaction.

---

## 🚀 Features

* 🎤 Real-time voice input (WebSocket streaming)
* 🧠 Speech-to-Text using Whisper
* 🤖 AI responses using Gemini
* 🔊 Text-to-Speech using Murf
* 🌐 Open websites using voice commands
* ♿ Accessibility automation using `hh.py`
* ⚡ Works as a browser extension (Edge)

---

## 🧩 How It Works

1. User speaks through microphone
2. Audio is streamed to backend
3. Whisper converts speech → text
4. Gemini generates response
5. System decides:

   * 🔊 Speak response
   * 🌐 Open website
6. Frontend plays audio OR opens URL

---

## 📂 Project Structure

```bash
echo-voice-assistant/
│
├── backend_ex/
│   ├── main.py
│   ├── chunk.webm
│   ├── api.txt
│   └── .env
│
├── frontend_ex/
│   ├── Index.html
│   ├── Index.js
│   ├── background.js
│   ├── manifest.json
│   ├── echo.ico
│   └── guide.txt
│
├── hh.py
├── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/Arp1it/Extension-B
cd Extension-B
```

### 2. Install Dependencies

```bash
pip install flask flask-cors flask-sock numpy openai-whisper soundfile murf google-genai pyautogui
```

---

## 🔐 Setup API Keys

Create a `.env` file inside `backend_ex/`:

```env
GEMINI_API_KEY=your_gemini_key
MURF_API_KEY=your_murf_key
```

⚠️ Never upload `.env` to GitHub.

---

## ▶️ Run Backend

```bash
python backend_ex/main.py
```

Server will start at:

```
http://127.0.0.1:5000
```

---

## 🌐 Run Frontend (Extension)

1. Open Edge
2. Go to:

```
edge://extensions/
```

3. Enable **Developer Mode**
4. Click **Load Unpacked**
5. Select `frontend_ex/` folder

---

## 🎤 Microphone Permission

Allow microphone access:

```
edge://settings/content/microphone
```

---

## 🧪 Example Voice Commands

* "open youtube"
* "open google"
* "what is python"
* "who is elon musk"

---

## 🤖 Command Format

When user says:

```
open youtube
```

AI responds:

```
https://youtube.com open
```

System detects this and opens the website automatically.

---

## ♿ Accessibility Script (`hh.py`)

This script helps blind users start everything without manual clicks.

### 🔥 What it does:

* Opens Microsoft Edge
* Focuses the browser
* Activates extension using `Ctrl + Space`

### ▶️ Run:

```bash
python hh.py
```

### ⚠️ Requirements:

* Edge browser installed
* Extension already loaded
* Screen timing may vary (adjust delays if needed)

---

## ⚠️ Known Issues

* ⏱️ ~4 second delay (audio buffering)
* 🔊 Browser autoplay restrictions
* 🎤 Mic permission needed first time

---

## 🚀 Future Improvements

* 🔥 Real-time streaming (no delay)
* 🔥 Hotword detection ("Hey Echo")
* 🔥 Open apps & system control
* 🔥 Search queries (YouTube, Google)
* 🔥 Interrupt AI while speaking

---

## 👨‍💻 Author

**Echo Cipher**
Cybersecurity Student | Developer | Builder

---

## ❤️ Purpose

Try to Built to make technology more accessible for blind users and reduce dependency on visual interaction.