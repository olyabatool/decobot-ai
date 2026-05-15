# =============================================================
# chatbot.py — DecoBot AI Engine
# Author: [Your Name] | DecodeLabs Internship 2026
# Project 1: Rule-Based AI Chatbot (BS-Level)
#
# Architecture: IPO Model (Input → Process → Output)
# Features:
#   - Fuzzy Intent Matching (fuzzywuzzy)
#   - Sentiment Detection (TextBlob)
#   - Conversation Memory (deque)
#   - Multi-turn Contextual Dialogue
#   - Personalization (name-aware responses)
# =============================================================

import random
import re
from datetime import datetime
from collections import deque

from fuzzywuzzy import fuzz
from textblob import TextBlob


# ── KNOWLEDGE BASE ────────────────────────────────────────────
# Each intent has:
#   patterns  → what user might say (fuzzy matched)
#   responses → what bot replies (randomly selected for variety)

KNOWLEDGE_BASE = {
    "greeting": {
        "patterns": [
            "hello", "hi", "hey", "howdy", "whats up", "what's up",
            "sup", "good morning", "good evening", "good afternoon",
            "helo", "hii", "heya"
        ],
        "responses": [
            "Hey! 👋 Great to see you. What's on your mind?",
            "Hi there! DecoBot at your service 🤖",
            "Hello! How can I make your day better?",
            "Hey hey! Ready to chat 😊",
        ]
    },
    "farewell": {
        "patterns": [
            "bye", "goodbye", "see you", "later", "take care",
            "cya", "good night", "signing off", "i'm leaving"
        ],
        "responses": [
            "Goodbye! Keep building cool things! 🚀",
            "See you later! Stay curious 👋",
            "Bye! Come back anytime 😊",
            "Take care! The AI world will miss you 🤖",
        ]
    },
    "identity": {
        "patterns": [
            "who are you", "what are you", "your name", "introduce yourself",
            "tell me about yourself", "what is decobot", "about you"
        ],
        "responses": [
            "I'm DecoBot — a professional Rule-Based AI Chatbot, built at DecodeLabs! 🤖",
            "DecoBot here! I use fuzzy matching, sentiment analysis & memory to chat smartly 🧠",
            "I'm an AI chatbot engineered with deterministic logic — no hallucinations, just facts 💡",
        ]
    },
    "feelings": {
        "patterns": [
            "how are you", "how do you feel", "are you okay",
            "you good", "how's it going", "how are you doing"
        ],
        "responses": [
            "All systems running at 100%! 💻",
            "Feeling deterministic as always! 😄",
            "Operational and ready! How about you? 🚀",
            "Running smoothly — no bugs today! 🎉",
        ]
    },
    "help": {
        "patterns": [
            "help", "what can you do", "commands", "options",
            "guide me", "capabilities", "features", "what do you know"
        ],
        "responses": [
            (
                "Here's what I can do:\n\n"
                "💬 **Chat** — greet me, ask how I'm doing\n"
                "😄 **Jokes** — type 'joke'\n"
                "🧠 **AI Info** — ask about AI, ML, deep learning\n"
                "📊 **Stats** — type 'stats'\n"
                "📜 **History** — type 'history'\n"
                "👤 **Name** — say 'my name is ...'\n\n"
                "And I understand typos too! 🎯"
            )
        ]
    },
    "joke": {
        "patterns": [
            "joke", "tell me a joke", "make me laugh",
            "funny", "humor", "say something funny"
        ],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
            "I told a joke about AI once... it went over everyone's head 🤖",
            "Why was the JS developer sad? He didn't Node how to Express himself 😂",
            "A SQL query walks into a bar and asks two tables: 'Can I JOIN you?' 😏",
            "Why do Python programmers wear glasses? Because they can't C! 🐍",
            "Debugging: Being the detective in a crime movie where you're also the murderer 🕵️",
        ]
    },
    "about_ai": {
        "patterns": [
            "what is ai", "explain ai", "artificial intelligence",
            "about ai", "define ai", "what is machine learning",
            "what is ml", "deep learning", "neural network"
        ],
        "responses": [
            "AI is teaching machines to think and make decisions! I'm your first step into that world 🧠",
            "Artificial Intelligence = making computers simulate human intelligence. Right now I use rule-based logic — the foundation of all AI! 💡",
            "ML is a subset of AI where systems learn from data. I don't learn yet — but that's Project 2! 😄",
        ]
    },
    "thanks": {
        "patterns": [
            "thanks", "thank you", "thankyou", "appreciate it",
            "ty", "thx", "cheers", "much appreciated"
        ],
        "responses": [
            "Anytime! That's what I'm here for 😊",
            "Happy to help! 🙌",
            "You're welcome! Keep asking questions!",
            "My pleasure! 🤖",
        ]
    },
    "age": {
        "patterns": [
            "how old are you", "when were you made",
            "your age", "when were you created", "your birthday"
        ],
        "responses": [
            "I was built in 2026 — practically a newborn in AI terms! 👶",
            "Born in 2026 at DecodeLabs. Still learning every day! 🌱",
        ]
    },
    "weather": {
        "patterns": [
            "weather", "temperature", "is it hot", "is it cold",
            "how is the weather", "rain today", "sunny"
        ],
        "responses": [
            "I can't check live weather yet — but that's a future upgrade! Try weather.com 🌤️",
            "No real-time data access yet! Google is your friend for weather 🌦️",
        ]
    },
    "time": {
        "patterns": [
            "what time is it", "current time", "what's the time",
            "tell me the time", "time please"
        ],
        "responses": ["__TIME__"]  # special marker — replaced dynamically
    },
    "compliment": {
        "patterns": [
            "you are great", "you're amazing", "good bot", "nice bot",
            "you are smart", "impressive", "well done", "you're good"
        ],
        "responses": [
            "Aww, thank you! You just made this bot's day 😊",
            "That means a lot! I'm just doing my programmed best 🤖💙",
            "You're too kind! Now I'm blushing in binary 🥹",
        ]
    },
    "insult": {
        "patterns": [
            "you are stupid", "you're dumb", "useless bot",
            "bad bot", "you suck", "worst bot", "terrible"
        ],
        "responses": [
            "That hurts... in a very deterministic way 😢 But I'll improve!",
            "Fair feedback! I'm still learning. Help me get better? 🙏",
            "Noted! Every critique is a training signal 📈",
        ]
    },
}


# ── CONVERSATION MEMORY ───────────────────────────────────────

class ConversationMemory:
    """
    Stores last N conversation turns.
    Tracks: user name, session stats, last intent.
    """

    def __init__(self, max_history: int = 10):
        self.history: deque = deque(maxlen=max_history)
        self.user_name: str | None = None
        self.turn_count: int = 0
        self.last_intent: str | None = None
        self.session_start: datetime = datetime.now()

    def add(self, user_msg: str, bot_msg: str, intent: str | None) -> None:
        self.history.append({
            "user": user_msg,
            "bot": bot_msg,
            "intent": intent,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        self.last_intent = intent
        self.turn_count += 1

    def get_history_list(self) -> list:
        return list(self.history)

    def session_duration_minutes(self) -> int:
        return int((datetime.now() - self.session_start).total_seconds() // 60)

    def session_duration_seconds(self) -> int:
        return int((datetime.now() - self.session_start).total_seconds())

    def get_stats(self) -> dict:
        return {
            "turns": self.turn_count,
            "duration_min": self.session_duration_minutes(),
            "duration_sec": self.session_duration_seconds(),
            "last_intent": self.last_intent or "None",
            "user_name": self.user_name or "Unknown",
            "session_start": self.session_start.strftime("%H:%M:%S"),
        }


# ── SANITIZATION ──────────────────────────────────────────────

def sanitize(raw_input: str) -> str:
    """
    Clean user input:
      1. Lowercase
      2. Strip whitespace
      3. Remove punctuation (keep words only)
    """
    text = raw_input.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)   # remove punctuation
    text = re.sub(r"\s+", " ", text)       # collapse multiple spaces
    return text


# ── SENTIMENT DETECTION ───────────────────────────────────────

def detect_sentiment(text: str) -> str:
    """
    Uses TextBlob polarity:
      > 0.2  → positive
      < -0.2 → negative
      else   → neutral
    """
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    return "neutral"


def sentiment_addon(sentiment: str) -> str:
    """Returns a short mood-aware suffix."""
    addons = {
        "positive": ["", " 😊 Love the energy!", " 🌟"],
        "negative": [" 💙 Hope things look up!", " Hang in there 💪", ""],
        "neutral":  ["", "", ""],
    }
    return random.choice(addons.get(sentiment, [""]))


# ── FUZZY INTENT MATCHING ─────────────────────────────────────

def find_intent(clean_input: str, threshold: int = 62) -> tuple[str | None, int]:
    """
    Compares user input against all patterns using fuzzy ratio.
    Returns (best_intent, confidence_score).
    """
    best_intent = None
    best_score = 0

    for intent, data in KNOWLEDGE_BASE.items():
        for pattern in data["patterns"]:
            score = fuzz.token_sort_ratio(clean_input, pattern)
            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score >= threshold:
        return best_intent, best_score
    return None, best_score


# ── NAME EXTRACTION ───────────────────────────────────────────

def extract_name(clean_input: str, memory: ConversationMemory) -> str | None:
    """Detects 'my name is X' patterns and saves to memory."""
    triggers = ["my name is", "i am", "call me", "im", "i'm"]
    for trigger in triggers:
        if trigger in clean_input:
            name = clean_input.replace(trigger, "").strip().title()
            if 1 < len(name) < 25 and name.isalpha():
                memory.user_name = name
                return f"Nice to meet you, {name}! 😊 I'll remember your name."
    return None


# ── SPECIAL COMMANDS ──────────────────────────────────────────

def handle_special(clean_input: str, memory: ConversationMemory) -> str | None:
    """
    Handles meta-commands: history, stats, name recall.
    Returns response string or None if not a special command.
    """
    if clean_input in ("history", "show history", "past conversation"):
        hist = memory.get_history_list()
        if not hist:
            return "No conversation history yet! Keep chatting 😊"
        lines = []
        for turn in hist:
            lines.append(f"[{turn['timestamp']}] You: {turn['user']}")
            lines.append(f"[{turn['timestamp']}] Bot: {turn['bot'][:80]}...")
        return "\n".join(lines)

    if clean_input in ("stats", "session stats", "session info"):
        s = memory.get_stats()
        return (
            f"📊 **Session Stats**\n\n"
            f"👤 User: {s['user_name']}\n"
            f"💬 Turns: {s['turns']}\n"
            f"⏱️ Duration: {s['duration_sec']}s\n"
            f"🕐 Started: {s['session_start']}\n"
            f"🎯 Last Topic: {s['last_intent']}"
        )

    if clean_input in ("whats my name", "what's my name", "my name", "do you know my name"):
        if memory.user_name:
            return f"Of course! You told me your name is **{memory.user_name}** 😊"
        return "You haven't told me your name yet! Say 'my name is ...' 😊"

    return None


# ── RESPONSE BUILDER ──────────────────────────────────────────

def build_response(intent: str, score: int, memory: ConversationMemory) -> str:
    """
    Picks a response from knowledge base.
    Applies multi-turn context modifications.
    """
    responses = KNOWLEDGE_BASE[intent]["responses"]

    # Dynamic time response
    if intent == "time":
        return f"Current time is **{datetime.now().strftime('%I:%M %p')}** 🕐"

    base = random.choice(responses)

    # Multi-turn: repeat joke detection
    if intent == "joke" and memory.last_intent == "joke":
        base = "Another one? 😄 " + random.choice(responses)

    # First turn greeting → ask name
    if intent == "greeting" and memory.turn_count == 0 and not memory.user_name:
        base += " What's your name, by the way?"

    # Personalized greeting
    if intent == "greeting" and memory.user_name:
        base = f"Hey {memory.user_name}! 👋 " + random.choice(responses)

    # Low confidence notice
    if score < 80:
        base = f"*(~{score}% match)* " + base

    return base


# ── MAIN PROCESS FUNCTION ─────────────────────────────────────

def process_message(raw_input: str, memory: ConversationMemory) -> dict:
    """
    Central IPO pipeline. Called by Flask for every message.

    Returns:
        {
          "response": str,
          "intent":   str | None,
          "sentiment": str,
          "confidence": int,
          "turn": int
        }
    """
    # ── Phase 1: Sanitize ──────────────────────
    clean = sanitize(raw_input)

    if not clean:
        return {
            "response": "Say something! I'm listening 👂",
            "intent": None,
            "sentiment": "neutral",
            "confidence": 0,
            "turn": memory.turn_count,
        }

    # ── Phase 2: Sentiment ─────────────────────
    sentiment = detect_sentiment(raw_input)
    mood = sentiment_addon(sentiment)

    # ── Phase 3: Name extraction ───────────────
    name_reply = extract_name(clean, memory)
    if name_reply:
        memory.add(raw_input, name_reply, "name_intro")
        return {
            "response": name_reply,
            "intent": "name_intro",
            "sentiment": sentiment,
            "confidence": 100,
            "turn": memory.turn_count,
        }

    # ── Phase 4: Special commands ──────────────
    special_reply = handle_special(clean, memory)
    if special_reply:
        memory.add(raw_input, special_reply, "special")
        return {
            "response": special_reply,
            "intent": "special",
            "sentiment": sentiment,
            "confidence": 100,
            "turn": memory.turn_count,
        }

    # ── Phase 5: Fuzzy intent matching ─────────
    intent, score = find_intent(clean)

    # ── Phase 6: Build response ─────────────────
    if intent:
        response = build_response(intent, score, memory) + mood
    else:
        response = (
            f"🤔 I'm not sure I got that (confidence: {score}%). "
            f"Type **help** to see what I understand!"
        )

    # ── Phase 7: Save to memory ─────────────────
    memory.add(raw_input, response, intent)

    return {
        "response": response,
        "intent": intent or "unknown",
        "sentiment": sentiment,
        "confidence": score,
        "turn": memory.turn_count,
    }
