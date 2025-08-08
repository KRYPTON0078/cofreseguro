"""Lightweight feature-based fraud scorer."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass


@dataclass
class MlResult:
    score: float
    features: dict[str, float]


WEIGHTS = {
    "len_norm": 0.05,
    "word_count_norm": 0.05,
    "url_count": 0.35,
    "digit_ratio": 0.15,
    "exclaim": 0.15,
    "upper_ratio": 0.2,
}


def score_text(text: str) -> MlResult:
    words = re.findall(r"\w+", text.lower())
    urls = re.findall(r"https?://", text.lower())
    digits = sum(ch.isdigit() for ch in text)
    feats = {
        "len_norm": min(len(text) / 400.0, 1.0),
        "word_count_norm": min(len(words) / 80.0, 1.0),
        "url_count": min(len(urls) / 3.0, 1.0),
        "digit_ratio": digits / max(len(text), 1),
        "exclaim": min(text.count("!") / 5.0, 1.0),
        "upper_ratio": sum(c.isupper() for c in text) / max(len(text), 1),
    }
    raw = sum(feats[k] * WEIGHTS[k] for k in WEIGHTS)
    score = 1.0 / (1.0 + math.exp(-6 * (raw - 0.35)))
    return MlResult(score=float(score), features=feats)
