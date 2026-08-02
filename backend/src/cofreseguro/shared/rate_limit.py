"""Simple in-memory rate limiter for demo deployments."""

from __future__ import annotations

import time
from collections import defaultdict, deque


class SlidingWindowLimiter:
    def __init__(self, max_requests: int = 60, window_s: float = 60.0) -> None:
        self.max_requests = max_requests
        self.window_s = window_s
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        q = self._hits[key]
        while q and now - q[0] > self.window_s:
            q.popleft()
        if len(q) >= self.max_requests:
            return False
        q.append(now)
        return True


analyze_limiter = SlidingWindowLimiter(max_requests=120, window_s=60.0)
