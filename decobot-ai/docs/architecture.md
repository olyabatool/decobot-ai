# DecoBot — Technical Architecture

## IPO Model

DecoBot follows the **Input → Process → Output** model described in the DecodeLabs curriculum.

### Input Phase: Sanitization
Raw user input is cleaned before any processing:
- `lower()` — normalize case
- `strip()` — remove leading/trailing whitespace
- `re.sub(r"[^\w\s]", "", text)` — remove punctuation

This ensures "Hello!", "HELLO", and "  hello  " all map to the same clean token `"hello"`.

### Process Phase: The Pipeline
1. **Sentiment Detection** — TextBlob analyzes emotional polarity
2. **Name Extraction** — regex-style pattern matching for "my name is X"
3. **Special Commands** — meta-queries like `stats`, `history`
4. **Fuzzy Intent Matching** — fuzzywuzzy compares against all patterns
5. **Response Building** — context-aware selection from knowledge base

### Output Phase: Response Generation
- Random selection from multiple responses per intent (variety)
- Mood-aware suffix appended based on sentiment
- Multi-turn modifications (e.g. repeat joke detection)
- Confidence score displayed in UI

## Data Structures

### Knowledge Base
```python
{
  "intent_name": {
    "patterns":  [str, ...],   # what user might say
    "responses": [str, ...],   # possible replies
  }
}
```

### ConversationMemory
```python
deque(maxlen=10)  # circular buffer, auto-drops oldest
{
  "user":      str,
  "bot":       str,
  "intent":    str | None,
  "timestamp": str,
}
```

## Algorithmic Complexity

| Approach | Lookup Complexity | Scalability |
|---|---|---|
| If-Elif chain | O(n) | Poor — degrades linearly |
| Dictionary `.get()` | O(1) | Excellent — constant time |

The knowledge base uses dictionary lookups after fuzzy matching, ensuring
the response retrieval step is always O(1) regardless of how many intents exist.

## Flask Session Management

Each browser session gets a UUID stored in a cookie. A server-side dictionary
maps `session_id → ConversationMemory`. This allows multiple users to have
isolated conversation histories simultaneously.

For production deployment, this in-memory store should be replaced with Redis.
