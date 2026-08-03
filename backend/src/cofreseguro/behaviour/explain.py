"""Explain behavioural risk score."""
from __future__ import annotations

def explain_behaviour(total: int, high: int, locale: str = "en") -> str:
    ratio = high / max(total, 1)
    if locale.startswith("pt"):
        return f"Perfil: {high}/{total} análises de alto risco (rácio {ratio:.2f})."
    return f"Profile: {high}/{total} high-risk analyses (ratio {ratio:.2f})."
