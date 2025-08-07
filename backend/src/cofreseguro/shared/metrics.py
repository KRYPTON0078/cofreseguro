"""Prometheus metrics."""

from prometheus_client import Counter, generate_latest

ANALYSES_TOTAL = Counter(
    "cofreseguro_analyses_total",
    "Total analyses",
    ["risk_level"],
)
LOGIN_TOTAL = Counter("cofreseguro_logins_total", "Total logins", ["result"])


def metrics_response() -> bytes:
    return generate_latest()
