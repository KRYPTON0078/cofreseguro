"""Ollama client — optional narrative enrichment."""

from __future__ import annotations

import httpx

from cofreseguro.shared.config import get_settings


async def enrich_with_llm(text: str, locale: str, risk_level: str) -> str | None:
    settings = get_settings()
    if not settings.ollama_enabled:
        return None
    lang = "Portuguese" if locale.startswith("pt") else "English"
    prompt = (
        f"You are a mobile-money fraud analyst. Reply in {lang} only. "
        f"Risk level is {risk_level}. Explain briefly why this message may be risky "
        f"and give one safety tip.\n\nMessage:\n{text[:1500]}"
    )
    try:
        async with httpx.AsyncClient(timeout=settings.ollama_timeout_s) as client:
            resp = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
            )
            if resp.status_code != 200:
                return None
            data = resp.json()
            return str(data.get("response", "")).strip() or None
    except Exception:
        return None
