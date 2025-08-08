"""Offline URL risk scoring."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd"}


@dataclass
class UrlScore:
    url: str
    score: float
    reasons: list[str]


def extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s]+", text, flags=re.IGNORECASE)


def score_url(url: str) -> UrlScore:
    reasons: list[str] = []
    score = 0.0
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if not host:
        return UrlScore(url, 0.4, ["malformed_url"])
    if host in SHORTENERS:
        score += 0.35
        reasons.append("url_shortener")
    if re.search(r"\d{1,3}(\.\d{1,3}){3}", host):
        score += 0.3
        reasons.append("raw_ip_host")
    if host.count("-") >= 2:
        score += 0.1
        reasons.append("many_hyphens")
    if len(host) > 40:
        score += 0.1
        reasons.append("long_host")
    if "mpesa" in host.replace("-", "") and not host.endswith((".mz", ".co.mz", ".com")):
        score += 0.2
        reasons.append("brand_lookalike:mpesa")
    return UrlScore(url, min(score, 1.0), reasons)


def score_urls_in_text(text: str) -> list[UrlScore]:
    return [score_url(u.rstrip(").,;")) for u in extract_urls(text)]
