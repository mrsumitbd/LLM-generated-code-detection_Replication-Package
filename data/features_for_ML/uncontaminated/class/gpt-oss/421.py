from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from collections import deque
from typing import Deque


@dataclass
class RateLimitTracker:
    """Track API rate limiting."""

    max_requests: int
    period: timedelta
    _timestamps: Deque[datetime] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._timestamps = deque(maxlen=self.max_requests)

    def _prune_old(self) -> None:
        """Remove timestamps that are older than the period."""
        now = datetime.now(timezone.utc)
        while self._timestamps and now - self._timestamps[0] > self.period:
            self._timestamps.popleft()

    def can_make_request(self) -> bool:
        """Return True if a new request can be made under the rate limit."""
        self._prune_old()
        return len(self._timestamps) < self.max_requests

    def record_request(self) -> None:
        """Record a request at the current time."""
        self._prune_old()
        if len(self._timestamps) >= self.max_requests:
            raise RuntimeError("Rate limit exceeded; cannot record request.")
        self._timestamps.append(datetime.now(timezone.utc))

    def time_until_reset(self) -> timedelta:
        """Return the time remaining until the next request is allowed."""
        self._prune_old()
        if len(self._timestamps) < self.max_requests:
            return timedelta(0)
        oldest = self._timestamps[0]
        reset_time = oldest + self.period
        now = datetime.now(timezone.utc)
        remaining = reset_time - now
        return remaining if remaining > timedelta(0) else timedelta(0)