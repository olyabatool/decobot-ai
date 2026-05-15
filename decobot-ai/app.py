# =============================================================
# app.py — DecoBot Flask Backend
# Author: [Your Name] | DecodeLabs Internship 2026
#
# Routes:
#   GET  /          → serves chat UI
#   POST /chat      → processes message, returns JSON
#   GET  /history   → returns conversation history
#   GET  /stats     → returns session stats
#   POST /reset     → resets conversation memory
# =============================================================

from flask import Flask, render_template, request, jsonify, session
from chatbot import process_message, ConversationMemory
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "decobot-secret-2026"   # for session management

# In-memory store: session_id → ConversationMemory
# (for a real app, use Redis or a database)
sessions: dict[str, ConversationMemory] = {}


def get_memory() -> ConversationMemory:
    """Get or create a ConversationMemory for the current browser session."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    sid = session["session_id"]
    if sid not in sessions:
        sessions[sid] = ConversationMemory()
    return sessions[sid]


# ── ROUTES ────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the chat UI."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Receives user message, runs through chatbot pipeline,
    returns JSON response.
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    memory = get_memory()
    result = process_message(user_message, memory)

    return jsonify({
        "response":   result["response"],
        "intent":     result["intent"],
        "sentiment":  result["sentiment"],
        "confidence": result["confidence"],
        "turn":       result["turn"],
        "timestamp":  datetime.now().strftime("%H:%M"),
    })


@app.route("/history", methods=["GET"])
def history():
    """Returns full conversation history as JSON."""
    memory = get_memory()
    return jsonify({
        "history": memory.get_history_list(),
        "total_turns": memory.turn_count,
    })


@app.route("/stats", methods=["GET"])
def stats():
    """Returns session stats as JSON."""
    memory = get_memory()
    return jsonify(memory.get_stats())


@app.route("/reset", methods=["POST"])
def reset():
    """Clears conversation memory for current session."""
    if "session_id" in session:
        sid = session["session_id"]
        if sid in sessions:
            del sessions[sid]
        del session["session_id"]
    return jsonify({"status": "reset", "message": "Conversation cleared! Fresh start 🚀"})


# ── ENTRY POINT ───────────────────────────────────────────────

if __name__ == "__main__":
    print("="*50)
    print("  🤖 DecoBot Server Starting...")
    print("  Open: http://127.0.0.1:5000")
    print("="*50)
    app.run(debug=True, host="0.0.0.0", port=5000)
