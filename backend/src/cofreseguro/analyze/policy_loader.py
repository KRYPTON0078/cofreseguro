"""Load YAML fraud rules and URL block fragments from policies/."""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import yaml

logger = logging.getLogger("cofreseguro.policies")


def _repo_root() -> Path:
    # backend/src/cofreseguro/analyze -> repo root
    return Path(__file__).resolve().parents[4]


@lru_cache
def load_rule_policies() -> list[dict]:
    rules_dir = _repo_root() / "policies" / "rules"
    out: list[dict] = []
    if not rules_dir.exists():
        return out
    for path in sorted(rules_dir.glob("rule_*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if data.get("enabled", True) and data.get("pattern"):
                out.append(data)
        except Exception as exc:  # noqa: BLE001
            logger.warning("skip rule %s: %s", path.name, exc)
    return out


@lru_cache
def load_url_fragments() -> list[dict]:
    url_dir = _repo_root() / "policies" / "url"
    out: list[dict] = []
    if not url_dir.exists():
        return out
    for path in sorted(url_dir.glob("blockish_*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if data.get("fragment"):
                out.append(data)
        except Exception as exc:  # noqa: BLE001
            logger.warning("skip url policy %s: %s", path.name, exc)
    return out


def clear_policy_cache() -> None:
    load_rule_policies.cache_clear()
    load_url_fragments.cache_clear()
