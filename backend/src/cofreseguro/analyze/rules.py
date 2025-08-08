"""Rule-based mobile-money fraud detection (EN + PT)."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class RuleHit:
    rule_id: str
    weight: float
    label: str


EN_PATTERNS: list[tuple[str, float, str]] = [
    (r"\b(urgent|immediately|act now)\b", 0.15, "urgency"),
    (r"\b(send (your )?pin|share (your )?pin|otp)\b", 0.35, "credential_harvest"),
    (r"\b(gift|prize|won|lottery)\b", 0.2, "prize_scam"),
    (r"\b(click (the )?link|verify account|confirm details)\b", 0.25, "phishing"),
    (r"\b(mpesa|m-pesa|mobile money)\b.*\b(agent)\b", 0.2, "fake_agent"),
    (r"https?://\S+", 0.15, "has_url"),
    (r"\b(bit\.ly|tinyurl|t\.co)/\S+", 0.25, "short_link"),
]

PT_PATTERNS: list[tuple[str, float, str]] = [
    (r"\b(urgente|imediatamente|aja agora)\b", 0.15, "urgency"),
    (r"\b(envie (o )?pin|partilhe (o )?pin|codigo otp|código otp)\b", 0.35, "credential_harvest"),
    (r"\b(premio|prémio|ganhou|loteria)\b", 0.2, "prize_scam"),
    (r"\b(clique no link|verifique a conta|confirme os dados)\b", 0.25, "phishing"),
    (r"\b(mpesa|m-pesa|dinheiro móvel)\b.*\b(agente)\b", 0.2, "fake_agent"),
    (r"https?://\S+", 0.15, "has_url"),
    (r"\b(bit\.ly|tinyurl|t\.co)/\S+", 0.25, "short_link"),
]


def evaluate_rules(text: str, locale: str = "en") -> tuple[float, list[RuleHit]]:
    patterns = PT_PATTERNS if locale.startswith("pt") else EN_PATTERNS
    combined = patterns + (EN_PATTERNS if locale.startswith("pt") else [])
    hits: list[RuleHit] = []
    score = 0.0
    seen: set[str] = set()
    lowered = text.lower()
    for pattern, weight, label in combined:
        if label in seen:
            continue
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            hits.append(RuleHit(rule_id=label, weight=weight, label=label))
            score += weight
            seen.add(label)
    return min(score, 1.0), hits
