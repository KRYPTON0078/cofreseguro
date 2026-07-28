"""Load literacy tips from docs/tips markdown and in-code bank."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from cofreseguro.literacy.tips import TIPS, tip_for


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@lru_cache
def load_tip_cards() -> list[dict]:
    tips_dir = _repo_root() / "docs" / "tips"
    cards: list[dict] = []
    if tips_dir.exists():
        for path in sorted(tips_dir.glob("tip_*.md")):
            text = path.read_text(encoding="utf-8")
            title = path.stem
            m = re.search(r"^#\s+(.+)$", text, flags=re.M)
            if m:
                title = m.group(1).strip()
            lang = "pt" if "(pt)" in title.lower() or "pt)" in title.lower() else "en"
            body = "\n".join(
                line for line in text.splitlines() if line.strip() and not line.startswith("#")
            ).strip()
            cards.append({"id": path.stem, "title": title, "locale": lang, "body": body})
    # Always include in-code tips as structured cards
    for label, locales in TIPS.items():
        if label == "default":
            continue
        for loc, body in locales.items():
            cards.append(
                {
                    "id": f"builtin-{label}-{loc}",
                    "title": f"{label} ({loc})",
                    "locale": loc,
                    "body": body,
                    "label": label,
                }
            )
    return cards


def tips_for_label(label: str, locale: str = "en") -> str:
    return tip_for([label], locale)


def clear_tip_cache() -> None:
    load_tip_cards.cache_clear()
