"""Lightweight fraud scorer with optional fitted weights from datasets."""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass
class MlResult:
    score: float
    features: dict[str, float]
    model: str = "lite-logistic"


DEFAULT_WEIGHTS = {
    "len_norm": 0.05,
    "word_count_norm": 0.05,
    "url_count": 0.35,
    "digit_ratio": 0.15,
    "exclaim": 0.15,
    "upper_ratio": 0.2,
    "pin_token": 0.4,
    "prize_token": 0.25,
    "urgency_token": 0.2,
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@lru_cache
def load_weights() -> tuple[dict[str, float], float, str]:
    artifact = _repo_root() / "backend" / "models" / "fraud_lite.json"
    if artifact.exists():
        data = json.loads(artifact.read_text(encoding="utf-8"))
        weights = {**DEFAULT_WEIGHTS, **(data.get("weights") or {})}
        bias = float(data.get("bias", 0.35))
        return weights, bias, str(data.get("name", "fraud-lite-fitted"))
    return DEFAULT_WEIGHTS, 0.35, "lite-logistic-default"


def extract_features(text: str) -> dict[str, float]:
    lowered = text.lower()
    words = re.findall(r"\w+", lowered)
    urls = re.findall(r"https?://", lowered)
    digits = sum(ch.isdigit() for ch in text)
    return {
        "len_norm": min(len(text) / 400.0, 1.0),
        "word_count_norm": min(len(words) / 80.0, 1.0),
        "url_count": min(len(urls) / 3.0, 1.0),
        "digit_ratio": digits / max(len(text), 1),
        "exclaim": min(text.count("!") / 5.0, 1.0),
        "upper_ratio": sum(c.isupper() for c in text) / max(len(text), 1),
        "pin_token": 1.0 if re.search(r"\b(pin|otp|codigo|código)\b", lowered) else 0.0,
        "prize_token": 1.0
        if re.search(r"\b(prize|premio|prémio|lottery|loteria|won|ganhou)\b", lowered)
        else 0.0,
        "urgency_token": 1.0
        if re.search(r"\b(urgent|urgente|immediately|imediatamente|asap)\b", lowered)
        else 0.0,
    }


def score_text(text: str) -> MlResult:
    weights, bias, name = load_weights()
    feats = extract_features(text)
    raw = sum(feats.get(k, 0.0) * weights.get(k, 0.0) for k in weights)
    score = 1.0 / (1.0 + math.exp(-6 * (raw - bias)))
    return MlResult(score=float(score), features=feats, model=name)
