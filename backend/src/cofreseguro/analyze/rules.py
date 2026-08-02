"""Rule-based mobile-money fraud detection (EN + PT + YAML policies)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from cofreseguro.analyze.policy_loader import load_rule_policies


@dataclass
class RuleHit:
    rule_id: str
    weight: float
    label: str


EN_PATTERNS: list[tuple[str, float, str, str]] = [
    (r"\b(urgent|immediately|act now|asap)\b", 0.15, "urgency", "builtin_en_urgency"),
    (r"\b(send (your )?pin|share (your )?pin|otp|one[- ]time (code|password))\b", 0.35, "credential_harvest", "builtin_en_pin"),
    (r"\b(gift|prize|won|lottery|jackpot|congratulations you)\b", 0.2, "prize_scam", "builtin_en_prize"),
    (r"\b(click (the )?link|verify account|confirm details|update (your )?kyc)\b", 0.25, "phishing", "builtin_en_phish"),
    (r"\b(mpesa|m-pesa|mobile money|emola|mkesh)\b.*\b(agent)\b", 0.2, "fake_agent", "builtin_en_agent"),
    (r"https?://\S+", 0.15, "has_url", "builtin_en_url"),
    (r"\b(bit\.ly|tinyurl|t\.co|goo\.gl)/\S+", 0.25, "short_link", "builtin_en_short"),
    (r"\b(account (suspended|blocked|limited)|unusual activity)\b", 0.22, "account_threat", "builtin_en_threat"),
    (r"\b(refund|tax refund|government grant)\b", 0.18, "refund_scam", "builtin_en_refund"),
    (r"\b(whatsapp|telegram).{0,40}\b(pay|pin|otp)\b", 0.2, "social_redirect", "builtin_en_social"),
]

PT_PATTERNS: list[tuple[str, float, str, str]] = [
    (r"\b(urgente|imediatamente|aja agora)\b", 0.15, "urgency", "builtin_pt_urgency"),
    (r"\b(envie (o )?pin|partilhe (o )?pin|codigo otp|código otp)\b", 0.35, "credential_harvest", "builtin_pt_pin"),
    (r"\b(premio|prémio|ganhou|loteria|parab[eé]ns)\b", 0.2, "prize_scam", "builtin_pt_prize"),
    (r"\b(clique no link|verifique a conta|confirme os dados|atualize (o )?kyc)\b", 0.25, "phishing", "builtin_pt_phish"),
    (r"\b(mpesa|m-pesa|dinheiro m[oó]vel|emola|mkesh)\b.*\b(agente)\b", 0.2, "fake_agent", "builtin_pt_agent"),
    (r"https?://\S+", 0.15, "has_url", "builtin_pt_url"),
    (r"\b(bit\.ly|tinyurl|t\.co)/\S+", 0.25, "short_link", "builtin_pt_short"),
    (r"\b(conta (suspensa|bloqueada|limitada)|atividade incomum)\b", 0.22, "account_threat", "builtin_pt_threat"),
    (r"\b(reembolso|imposto|subs[ií]dio)\b", 0.18, "refund_scam", "builtin_pt_refund"),
    (r"\b(whatsapp|telegram).{0,40}\b(pague|pin|otp)\b", 0.2, "social_redirect", "builtin_pt_social"),
]


def _yaml_patterns(locale: str) -> list[tuple[str, float, str, str]]:
    out: list[tuple[str, float, str, str]] = []
    for rule in load_rule_policies():
        locales = rule.get("locales") or ["en", "pt"]
        if locale[:2] not in locales and "en" not in locales:
            continue
        pattern = rule.get("pattern") or ""
        weight = float(rule.get("weight") or 0.1)
        label = str(rule.get("label") or rule.get("id") or "policy")
        rid = str(rule.get("id") or label)
        out.append((pattern, weight, label, rid))
    return out


def evaluate_rules(text: str, locale: str = "en") -> tuple[float, list[RuleHit]]:
    patterns = PT_PATTERNS if locale.startswith("pt") else EN_PATTERNS
    combined = list(patterns)
    if locale.startswith("pt"):
        combined.extend(EN_PATTERNS)
    combined.extend(_yaml_patterns(locale))
    hits: list[RuleHit] = []
    score = 0.0
    seen: set[str] = set()
    lowered = text.lower()
    for pattern, weight, label, rid in combined:
        key = f"{label}:{rid}"
        if key in seen or label in seen:
            continue
        try:
            if re.search(pattern, lowered, flags=re.IGNORECASE):
                hits.append(RuleHit(rule_id=rid, weight=weight, label=label))
                score += weight
                seen.add(label)
                seen.add(key)
        except re.error:
            continue
    return min(score, 1.0), hits
