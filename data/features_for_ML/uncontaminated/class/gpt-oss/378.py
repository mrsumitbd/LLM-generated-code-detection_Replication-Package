import time
from collections import deque
from typing import Deque


class CommandRateLimiter:
    """Rate limiter for OVMS commands.

    Prevents sending too many commands in a short period to avoid overwhelming the OVMS module.
    """

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        if max_calls <= 0:
            raise ValueError("max_calls must be positive")
        if period <= 0:
            raise ValueError("period must be positive")
        self.max_calls: int = max_calls
        self.period: float = period
        self._calls: Deque[float] = deque()

    def _prune_old_calls(self) -> None:
        """Remove timestamps older than the current period."""
        now = time.time()
        while self._calls and now - self._calls[0] >= self.period:
            self._calls.popleft()

    def can_call(self) -> bool:
        """Return True if a new command can be sent now, otherwise False.
        If True, the call is recorded for future rate limiting."""
        self._prune_old_calls()
        if len(self._calls) < self.max_calls:
            self._calls.append(time.time())
            return True
        return False

    def calls_remaining(self) -> int:
        """Return the number of calls still allowed in the current period."""
        self._prune_old_calls()
        return max(0, self.max_calls - len(self._calls))

    def time_to_next_call(self) -> float:
        """Return the number of seconds until the next call is allowed.
        If a call can be made immediately, returns 0.0."""
        self._prune_old_calls()
        if len(self._calls) < self.max_calls:
            return 0.0
        now = time.time()
        earliest = self._calls[0]
        wait = self.period - (now - earliest)
        return max(0.0, wait)