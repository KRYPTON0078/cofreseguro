#!/usr/bin/env python3
"""Fit lightweight logistic weights from EN/PT datasets into backend/models/fraud_lite.json."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def features(text: str) -> dict[str, float]:
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


def load_samples() -> list[tuple[dict[str, float], float]]:
    rows: list[tuple[dict[str, float], float]] = []
    for locale in ("en", "pt"):
        for path in sorted((ROOT / "datasets" / locale).glob("sample_*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            label = 1.0 if data.get("label") in {"fraud", "scam", 1, "1"} else 0.0
            # synthetic set is mostly fraud; treat "ham"/"legit" as 0
            if data.get("label") in {"ham", "legit", "safe"}:
                label = 0.0
            rows.append((features(str(data.get("text", ""))), label))
    # add a few hard negatives
    for text in (
        "Your M-Pesa balance is 250.00 MT. Dial *150# for more.",
        "Pagamento recebido 100 MT de Ana. Obrigado.",
        "Reminder: keep your PIN private. Official tip from support education.",
    ):
        rows.append((features(text), 0.0))
    return rows


def fit(rows: list[tuple[dict[str, float], float]]) -> dict:
    keys = list(rows[0][0].keys())
    weights = {k: 0.1 for k in keys}
    bias = 0.35
    lr = 0.35
    for _ in range(80):
        for feats, y in rows:
            raw = sum(feats[k] * weights[k] for k in keys) - bias
            pred = 1.0 / (1.0 + math.exp(-raw))
            err = pred - y
            for k in keys:
                weights[k] -= lr * err * feats[k]
            bias += lr * err * 0.05
    # normalize into ml_scorer expected space (positive weights)
    weights = {k: max(0.02, abs(v)) for k, v in weights.items()}
    return {"name": "fraud-lite-fitted", "bias": 0.35, "weights": weights, "n_samples": len(rows)}


def main() -> None:
    rows = load_samples()
    model = fit(rows)
    out = ROOT / "backend" / "models" / "fraud_lite.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} from {model['n_samples']} samples")


if __name__ == "__main__":
    main()
