import time

class CommandRateLimiter:
    """Rate limiter for OVMS commands.

    Prevents sending too many commands in a short period to avoid overwhelming the OVMS module.
    """

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = 0
        self.last_call_time = 0

    def can_call(self) -> bool:
        current_time = time.time()
        if self.calls < self.max_calls or current_time - self.last_call_time > self.period:
            self.calls += 1
            self.last_call_time = current_time
            return True
        return False

    def calls_remaining(self) -> int:
        return max(0, self.max_calls - self.calls)

    def time_to_next_call(self) -> float:
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        return max(0, self.period - time_since_last_call)