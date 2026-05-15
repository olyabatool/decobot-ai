// =============================================================
// chat.js — DecoBot Frontend Logic
// Author: [Your Name] | DecodeLabs Internship 2026
//
// Responsibilities:
//   - Send messages to Flask /chat endpoint
//   - Render bot & user messages in the DOM
//   - Update metadata chips (sentiment, intent, confidence)
//   - Handle History and Stats panel loading
//   - Manage nav tab switching
// =============================================================

"use strict";

// ── DOM REFERENCES ────────────────────────────────────────────
const messagesEl   = document.getElementById("messages");
const inputEl      = document.getElementById("user-input");
const sendBtn      = document.getElementById("send-btn");

const valSentiment = document.getElementById("val-sentiment");
const valIntent    = document.getElementById("val-intent");
const valConf      = document.getElementById("val-conf");
const chipSentiment= document.getElementById("chip-sentiment");

const btnChat      = document.getElementById("btn-chat");
const btnHistory   = document.getElementById("btn-history");
const btnStats     = document.getElementById("btn-stats");
const btnReset     = document.getElementById("btn-reset");

const panelChat    = document.getElementById("panel-chat");
const panelHistory = document.getElementById("panel-history");
const panelStats   = document.getElementById("panel-stats");
const historyList  = document.getElementById("history-list");


// ── HELPERS ───────────────────────────────────────────────────

/** Scroll messages container to bottom */
function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

/** Escape HTML to prevent XSS */
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/**
 * Render basic markdown-like formatting in bot messages:
 *   **text** → <strong>
 *   `code`   → <code>
 *   \n       → <br>
 */
function formatText(text) {
  return escapeHtml(text)
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/`(.*?)`/g, "<code>$1</code>")
    .replace(/\n/g, "<br>");
}

/** Current time as HH:MM */
function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}


// ── MESSAGE RENDERING ─────────────────────────────────────────

function appendMessage(role, text, meta = {}) {
  const isBot  = role === "bot";
  const time   = meta.time || timeNow();
  const label  = isBot ? "DecoBot" : "You";
  const avatar = isBot ? "⬡" : "👤";

  const div = document.createElement("div");
  div.className = `msg msg--${role}`;
  div.innerHTML = `
    <div class="msg__avatar">${avatar}</div>
    <div class="msg__body">
      <div class="msg__bubble">${isBot ? formatText(text) : escapeHtml(text)}</div>
      <div class="msg__meta">${label} · ${time}</div>
    </div>
  `;

  messagesEl.appendChild(div);
  scrollToBottom();
}

function showTyping() {
  const div = document.createElement("div");
  div.className = "msg msg--bot typing-indicator";
  div.id = "typing";
  div.innerHTML = `
    <div class="msg__avatar">⬡</div>
    <div class="msg__body">
      <div class="msg__bubble">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
    </div>
  `;
  messagesEl.appendChild(div);
  scrollToBottom();
}

function removeTyping() {
  const el = document.getElementById("typing");
  if (el) el.remove();
}


// ── METADATA CHIPS ────────────────────────────────────────────

const sentimentColors = {
  positive: "#00ff88",
  negative: "#ff4455",
  neutral:  "#7a9bb0",
};

function updateChips(data) {
  valSentiment.textContent = data.sentiment || "—";
  valIntent.textContent    = (data.intent || "—").replace("_", " ");
  valConf.textContent      = data.confidence ? `${data.confidence}%` : "—";

  // Tint sentiment chip
  const color = sentimentColors[data.sentiment] || "#7a9bb0";
  valSentiment.style.color = color;
}


// ── SEND MESSAGE ──────────────────────────────────────────────

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  // Render user message
  appendMessage("user", text);
  inputEl.value = "";
  inputEl.focus();

  // Show typing
  showTyping();
  sendBtn.disabled = true;

  try {
    const res  = await fetch("/chat", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ message: text }),
    });

    const data = await res.json();
    removeTyping();

    if (data.error) {
      appendMessage("bot", "⚠️ Something went wrong. Please try again.");
      return;
    }

    // Render bot message
    appendMessage("bot", data.response, { time: data.timestamp });

    // Update metadata chips
    updateChips(data);

  } catch (err) {
    removeTyping();
    appendMessage("bot", "⚠️ Network error — is the server running?");
    console.error("Fetch error:", err);
  } finally {
    sendBtn.disabled = false;
  }
}


// ── HISTORY PANEL ─────────────────────────────────────────────

async function loadHistory() {
  try {
    const res  = await fetch("/history");
    const data = await res.json();

    historyList.innerHTML = "";

    if (!data.history || data.history.length === 0) {
      historyList.innerHTML = `<p class="empty-state">No history yet. Start chatting! 💬</p>`;
      return;
    }

    data.history.forEach(turn => {
      const sentClass = {
        positive: "tag--pos",
        negative: "tag--neg",
        neutral:  "tag--neu",
      }[turn.sentiment] || "tag--neu";

      const item = document.createElement("div");
      item.className = "history-item";
      item.innerHTML = `
        <div class="history-item__user">
          <span>[${turn.timestamp || "—"}] You:</span>
          ${escapeHtml(turn.user)}
        </div>
        <div class="history-item__bot">
          <span>Bot:</span>
          ${escapeHtml((turn.bot || "").substring(0, 100))}${(turn.bot || "").length > 100 ? "..." : ""}
        </div>
        <div class="history-item__meta">
          <span class="tag tag--intent">${(turn.intent || "unknown").replace("_", " ")}</span>
        </div>
      `;
      historyList.appendChild(item);
    });
  } catch (err) {
    historyList.innerHTML = `<p class="empty-state">Failed to load history ⚠️</p>`;
    console.error(err);
  }
}


// ── STATS PANEL ───────────────────────────────────────────────

async function loadStats() {
  try {
    const res  = await fetch("/stats");
    const data = await res.json();

    document.getElementById("stat-turns").textContent    = data.turns       ?? "—";
    document.getElementById("stat-duration").textContent = data.duration_sec ?? "—";
    document.getElementById("stat-intent").textContent   = (data.last_intent || "—").replace("_", " ");
    document.getElementById("stat-user").textContent     = data.user_name   ?? "—";
    document.getElementById("stat-start").textContent    = data.session_start ?? "—";
  } catch (err) {
    console.error("Stats fetch error:", err);
  }
}


// ── RESET ─────────────────────────────────────────────────────

async function resetSession() {
  if (!confirm("Reset session? This will clear conversation history.")) return;

  try {
    await fetch("/reset", { method: "POST" });
    messagesEl.innerHTML = "";
    appendMessage("bot", "Session reset! Fresh start 🚀 What's on your mind?");
    valSentiment.textContent = "—";
    valIntent.textContent    = "—";
    valConf.textContent      = "—";
    valSentiment.style.color = "";
  } catch (err) {
    console.error("Reset error:", err);
  }
}


// ── NAV TABS ──────────────────────────────────────────────────

function switchTab(activeBtn, activePanel) {
  // Buttons
  [btnChat, btnHistory, btnStats].forEach(b => b.classList.remove("nav-btn--active"));
  activeBtn.classList.add("nav-btn--active");

  // Panels
  [panelChat, panelHistory, panelStats].forEach(p => p.classList.remove("panel--active"));
  activePanel.classList.add("panel--active");
}


// ── EVENT LISTENERS ───────────────────────────────────────────

sendBtn.addEventListener("click", sendMessage);

inputEl.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

btnChat.addEventListener("click", () => {
  switchTab(btnChat, panelChat);
});

btnHistory.addEventListener("click", () => {
  switchTab(btnHistory, panelHistory);
  loadHistory();
});

btnStats.addEventListener("click", () => {
  switchTab(btnStats, panelStats);
  loadStats();
});

btnReset.addEventListener("click", resetSession);

// Auto-focus input on load
inputEl.focus();
