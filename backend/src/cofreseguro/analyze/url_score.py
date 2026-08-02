"""Offline URL risk scoring with policy fragments."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

from cofreseguro.analyze.policy_loader import load_url_fragments

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "cutt.ly", "rb.gy"}


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
    path = (parsed.path or "").lower()
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
    brand_tokens = ("mpesa", "vodacom", "emola", "mkesh", "paypal", "banco")
    for brand in brand_tokens:
        compact = host.replace("-", "").replace(".", "")
        if brand in compact and not host.endswith((".mz", ".co.mz", ".com", ".co.za")):
            score += 0.2
            reasons.append(f"brand_lookalike:{brand}")
            break
    for frag in load_url_fragments():
        fragment = str(frag.get("fragment") or "").lower()
        if fragment and (fragment in host or fragment in path or fragment in url.lower()):
            score += float(frag.get("weight") or 0.15)
            reasons.append(f"policy_fragment:{frag.get('id', 'frag')}")
    return UrlScore(url, min(score, 1.0), reasons)


def score_urls_in_text(text: str) -> list[UrlScore]:
    return [score_url(u.rstrip(").,;")) for u in extract_urls(text)]
