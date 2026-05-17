# 🤖 DecoBot — Rule-Based AI Chatbot

> **DecodeLabs Industrial Training Kit · Batch 2026 · Project 1**

A professional, full-stack Rule-Based AI Chatbot built with Python + Flask.
Goes beyond basic if-else logic to implement a production-grade architecture
with fuzzy intent matching, sentiment detection, conversation memory, and a
dark-themed web GUI.

---

## 🖥️ Preview

```
╔══════════════════════════════════════════╗
║  ⬡ DecoBot  |  v2.0 · Rule-Based AI     ║
║  MOOD: positive  INTENT: joke  CONF: 94% ║
╠══════════════════════════════════════════╣
║  You:  tell me something funny           ║
║  Bot:  Why do programmers prefer dark    ║
║        mode? Because light attracts      ║
║        bugs! 😄                          ║
╚══════════════════════════════════════════╝
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Fuzzy Matching** | Understands typos and variations using `fuzzywuzzy` |
| 💬 **Conversation Memory** | Remembers last 10 exchanges per session |
| 😊 **Sentiment Detection** | Detects user mood via `TextBlob` |
| 🔄 **Multi-turn Dialogue** | Context-aware, personalized responses |
| 🌐 **Web GUI** | Dark-themed professional interface (Flask + HTML/CSS/JS) |
| 📊 **Live Stats** | Real-time session analytics |
| 📜 **History Panel** | Full conversation log with intent tags |
| 🔁 **Session Reset** | Clean restart without server reload |

---

## 🏗️ Architecture

```
USER INPUT
    │
    ▼
┌─────────────┐
│ SANITIZATION│  lowercase · strip · remove punctuation
└──────┬──────┘
       │
    ▼
┌─────────────────┐
│ SENTIMENT       │  TextBlob polarity → positive / negative / neutral
└──────┬──────────┘
       │
    ▼
┌─────────────────┐
│ NAME DETECTION  │  "my name is X" → stored in memory
└──────┬──────────┘
       │
    ▼
┌─────────────────┐
│ SPECIAL CMDS    │  history · stats · name recall
└──────┬──────────┘
       │
    ▼
┌─────────────────┐
│ FUZZY MATCHING  │  fuzz.token_sort_ratio against all patterns O(1) dict
└──────┬──────────┘
       │
    ▼
┌─────────────────┐
│ RESPONSE BUILD  │  random selection · multi-turn context · personalization
└──────┬──────────┘
       │
    ▼
  OUTPUT + memory.add()
```

---

## 📁 Project Structure

```
decobot-ai/
│
├── app.py                  Flask backend (routes & session management)
├── chatbot.py              Core AI engine (IPO pipeline)
├── requirements.txt        Python dependencies
├── README.md               This file
│
├── templates/
│   └── index.html          Chat UI (Jinja2 template)
│
├── static/
│   ├── css/
│   │   └── style.css       Dark retro-futuristic theme
│   └── js/
│       └── chat.js         Frontend logic (fetch API + DOM)
│
└── docs/
    └── architecture.md     Detailed technical documentation
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/decobot-ai.git
cd decobot-ai
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

---

## 💬 Supported Intents

| Intent | Example Inputs |
|---|---|
| `greeting` | hello, hi, hey, good morning |
| `farewell` | bye, goodbye, see you |
| `identity` | who are you, your name |
| `feelings` | how are you, you good? |
| `help` | help, what can you do |
| `joke` | joke, make me laugh, funny |
| `about_ai` | what is AI, explain ML |
| `thanks` | thanks, appreciate it |
| `time` | what time is it |
| `compliment` | good bot, you're amazing |
| `insult` | bad bot, you're dumb |

---

## 🧪 Key Concepts Demonstrated

### Why Dictionary over If-Elif?

```python
# ❌ Anti-pattern: O(n) — slows down with more rules
if   user_input == "hello": ...
elif user_input == "bye":   ...
elif user_input == "help":  ...   # checks every condition

# ✅ Professional: O(1) — instant lookup regardless of size
responses = {"hello": "Hi!", "bye": "Goodbye!"}
reply = responses.get(user_input, "I don't understand")
```

### Fuzzy Matching
```python
# Handles typos and variations
fuzz.token_sort_ratio("helo", "hello")   # → 89
fuzz.token_sort_ratio("make me laugh", "joke")  # → 63+
```

### Sentiment Detection
```python
TextBlob("I love this!").sentiment.polarity   # → 0.625 (positive)
TextBlob("this is terrible").sentiment.polarity  # → -1.0 (negative)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Flask 3.0 |
| AI Engine | fuzzywuzzy, TextBlob, python-Levenshtein |
| Frontend | HTML5, CSS3 (custom dark theme), Vanilla JS |
| Fonts | Syne (display), Space Mono (body) |

---

## 📈 What's Next (Project 2 Preview)

Project 1 uses **discrete key-value mapping** (exact + fuzzy).
Project 2 will upgrade to **semantic vector embeddings** — where meaning
is represented as coordinates in high-dimensional space, enabling true
contextual understanding.

```
Project 1:  "hello" ──────────► "Hi there!"  (key lookup)
Project 2:  "hello" → [0.2, 0.9, 0.4] → nearest vector → response
```

---
