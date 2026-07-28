"""Tips HTTP API."""

from __future__ import annotations

from fastapi import APIRouter, Query

from cofreseguro.literacy.loader import load_tip_cards, tips_for_label

router = APIRouter(prefix="/v1/tips", tags=["tips"])


@router.get("")
async def list_tips(locale: str | None = Query(default=None)) -> list[dict]:
    cards = load_tip_cards()
    if locale:
        cards = [c for c in cards if c.get("locale", "en").startswith(locale[:2])]
    return cards


@router.get("/by-label/{label}")
async def tip_by_label(label: str, locale: str = "en") -> dict:
    return {"label": label, "locale": locale, "tip": tips_for_label(label, locale)}
