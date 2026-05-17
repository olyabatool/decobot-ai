<div align="center">

<br>

# 🤖 DecoBot AI

### Rule-Based Chatbot — DecodeLabs Internship 2026

<br>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![FuzzyWuzzy](https://img.shields.io/badge/Fuzzy-Matching-FF6B6B?style=for-the-badge&logoColor=white)]()
[![TextBlob](https://img.shields.io/badge/TextBlob-Sentiment-4ECDC4?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)]()

<br>

> *"Before you build systems that learn on their own, master the art of teaching a machine through explicit logic."*
> — DecodeLabs Curriculum

<br>

</div>

---

## 📌 Overview

**DecoBot** is a full-stack, professional-grade Rule-Based AI Chatbot — built as **Project 1** of the DecodeLabs AI Internship Track 2026.

It goes far beyond basic if-else logic. This project implements a production-quality **IPO pipeline** (Input → Process → Output) with fuzzy intent matching, real-time sentiment analysis, conversation memory, and a live dark-themed web interface — all powered by deterministic rule-based logic, no neural networks needed.

This is the same **guardrail architecture** used in real AI systems like NVIDIA NeMo and Llama Guard — the control layer that sits on top of large language models in production.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **Fuzzy Intent Matching** | Handles typos and variations — `"helo"` correctly maps to `"hello"` |
| 😊 **Sentiment Detection** | Detects user mood in real time using TextBlob polarity analysis |
| 🧠 **Conversation Memory** | Stores last 10 exchanges per session using a circular `deque` buffer |
| 🔄 **Multi-turn Dialogue** | Context-aware responses — detects repeated intents and personalizes replies |
| 👤 **Name Personalization** | Learns your name mid-conversation and uses it throughout |
| 🌐 **Dark Web GUI** | Retro-futuristic chat interface with 3 panels: Chat, History, Stats |
| 📊 **Live Session Analytics** | Real-time stats — turn count, session duration, last detected intent |
| 📜 **History Panel** | Full conversation log with intent and sentiment tags per message |
| 🔁 **Session Reset** | One-click fresh start without restarting the server |

---

## 🖥️ Interface Preview

```
╔══════════════════════════════════════════════════════════╗
║  ⬡ DecoBot  │  v2.0 · Rule-Based AI                     ║
║─────────────────────────────────────────────────────────║
║  MOOD: positive 🟢   INTENT: joke   CONF: 94%           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   ⬡  Hey Sara! 👋 Great to see you again.               ║
║                                                          ║
║                   tell me something funny  [You] →      ║
║                                                          ║
║   ⬡  Why do programmers prefer dark mode?               ║
║       Because light attracts bugs! 😄                   ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  [ Type a message...                        ] [ Send → ] ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🏗️ Architecture — IPO Model

The entire chatbot follows the **Input → Process → Output** model taught in the DecodeLabs curriculum:

```
USER INPUT
    │
    ▼
┌──────────────────────────────────┐
│  SANITIZATION                    │
│  .lower() · .strip() · regex     │
│  "HELLO!!" ──► "hello"           │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  SENTIMENT DETECTION             │
│  TextBlob polarity score         │
│  > 0.2  → positive 😊           │
│  < -0.2 → negative 😔           │
│  else   → neutral  😐           │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  NAME EXTRACTION                 │
│  "my name is Sara" → saved ✅    │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  SPECIAL COMMANDS                │
│  history · stats · name recall   │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  FUZZY INTENT MATCHING           │
│  fuzz.token_sort_ratio()         │
│  threshold: 62 · O(1) lookup     │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│  RESPONSE BUILDING               │
│  Random pick · Multi-turn ctx    │
│  Personalization · Mood addon    │
└──────────────┬───────────────────┘
               │
               ▼
         OUTPUT + MEMORY UPDATE
```

### Dictionary vs If-Elif — Why it matters

```python
# ❌ Anti-Pattern — O(n) Linear Complexity
# Checks every single condition — gets slower with more rules
if   user_input == "hello": ...
elif user_input == "bye":   ...
elif user_input == "help":  ...
elif user_input == "joke":  ...   # still checking...


# ✅ Professional Approach — O(1) Constant Time
# Instant lookup regardless of how many intents exist
responses = {
    "hello": "Hi there!",
    "bye":   "Goodbye!",
    "help":  "Here's what I can do...",
}
reply = responses.get(user_input, "I don't understand.")
```

---

## 📁 Project Structure

```
decobot-ai/
│
├── app.py                   Flask server — 5 REST API routes
├── chatbot.py               Core AI engine — full IPO pipeline
├── requirements.txt         Python dependencies
├── README.md                Project documentation
│
├── templates/
│   └── index.html           Dark-theme chat UI (3 panels)
│
├── static/
│   ├── css/
│   │   └── style.css        Retro-futuristic dark styling
│   └── js/
│       └── chat.js          Frontend logic — Fetch API
│
└── docs/
    └── architecture.md      Deep-dive technical documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/olyabatool/decobot-ai.git
cd decobot-ai
```

**2. Create a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the server**
```bash
python app.py
```

**5. Open in browser**
```
http://127.0.0.1:5000
```

---

## 💬 Supported Intents

| Intent | Example Phrases |
|---|---|
| `greeting` | hello, hi, hey, good morning, helo *(typo ok!)* |
| `farewell` | bye, goodbye, see you, take care |
| `identity` | who are you, your name, introduce yourself |
| `feelings` | how are you, you good, how's it going |
| `help` | help, what can you do, commands |
| `joke` | joke, tell me a joke, make me laugh, funny |
| `about_ai` | what is AI, explain machine learning, deep learning |
| `thanks` | thanks, thank you, ty, appreciate it |
| `time` | what time is it, current time |
| `compliment` | good bot, you're amazing, impressive |
| `insult` | bad bot, you're dumb *(handled gracefully!)* |

> All intents support **fuzzy matching** — partial phrases, typos, and variations all work.

---

## 🛠️ Tech Stack

| Layer | Technology | Role |
|---|---|---|
| Backend | Python 3.11 + Flask 3.0 | Server + REST API |
| Fuzzy Matching | fuzzywuzzy + python-Levenshtein | Typo-tolerant intent detection |
| NLP | TextBlob | Sentiment polarity analysis |
| Memory | Python `collections.deque` | Circular conversation buffer |
| Frontend | HTML5 + CSS3 + Vanilla JS | Dark theme GUI |
| Typography | Syne + Space Mono (Google Fonts) | Retro-futuristic design |

---

## 🔌 API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Serves the chat UI |
| `POST` | `/chat` | Processes message, returns JSON response |
| `GET` | `/history` | Returns full conversation history |
| `GET` | `/stats` | Returns session statistics |
| `POST` | `/reset` | Clears conversation memory |

**Example `/chat` response:**
```json
{
  "response":   "Hey Sara! 👋 Great to see you.",
  "intent":     "greeting",
  "sentiment":  "positive",
  "confidence": 97,
  "turn":       3,
  "timestamp":  "02:45 PM"
}
```

---

## 📈 Project Roadmap

```
✅  Project 1  —  Rule-Based Chatbot      (Fuzzy + Sentiment + Memory)
🔜  Project 2  —  Semantic Chatbot        (Word Embeddings + Vector Search)
🔜  Project 3  —  ML Intent Classifier    (scikit-learn + TF-IDF)
🔜  Project 4  —  Neural Chatbot          (Transformer Architecture)
```

---

## 🧠 Key Learnings

Working on this project demonstrated:

- The **IPO model** as a foundation for all AI system design
- Why **deterministic guardrails** are essential in production AI
- The performance advantage of **hash maps over linear search** (O(1) vs O(n))
- How **fuzzy string matching** bridges the gap between rule-based and ML systems
- **Session management** in web applications using Flask + UUID
- Full-stack development — Python backend + HTML/CSS/JS frontend

---

## 👩‍💻 Author

**Olya Batool**
AI Engineer Intern · DecodeLabs Batch 2026

[![GitHub](https://img.shields.io/badge/GitHub-olyabatool-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/olyabatool)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/your-linkedin)

---

## 📄 License

```
MIT License
Copyright (c) 2026 Olya Batool
Free to use, modify, and share with attribution.
```

---

<div align="center">

Built with 💙 during the DecodeLabs AI Internship · Project 1 of 4

</div>
