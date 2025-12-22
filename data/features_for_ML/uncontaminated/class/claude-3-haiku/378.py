import time

class CommandRateLimiter:
    """Rate limiter for OVMS commands.

    Prevents sending too many commands in a short period to avoid overwhelming the OVMS module.
    """

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.call_times = []

    def can_call(self) -> bool:
        now = time.time()
        self.call_times = [t for t in self.call_times if t > now - self.period]
        if len(self.call_times) < self.max_calls:
            self.call_times.append(now)
            return True
        return False

    def calls_remaining(self) -> int:
        now = time.time()
        self.call_times = [t for t in self.call_times if t > now - self.period]
        return self.max_calls - len(self.call_times)

    def time_to_next_call(self) -> float:
        now = time.time()
        self.call_times = [t for t in self.call_times if t > now - self.period]
        if len(self.call_times) >= self.max_calls:
            return self.call_times[0] + self.period - now
        return 0.0