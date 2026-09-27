"""Small deterministic sentiment utility for retrieved news text."""
from __future__ import annotations

import re
from typing import Any

POSITIVE = {"beat", "growth", "gain", "bullish", "strong", "upgrade", "profit", "record", "outperform"}
NEGATIVE = {"miss", "loss", "bearish", "weak", "downgrade", "risk", "decline", "lawsuit", "cut"}


def analyze_sentiment(text: str) -> dict[str, Any]:
    """Score financial text using a transparent lexical baseline."""
    words = re.findall(r"[a-zA-Z']+", text.lower())
    positive, negative = sum(word in POSITIVE for word in words), sum(word in NEGATIVE for word in words)
    score = positive - negative
    label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return {"sentiment": label, "score": score, "positive_terms": positive, "negative_terms": negative, "method": "lexical baseline"}
