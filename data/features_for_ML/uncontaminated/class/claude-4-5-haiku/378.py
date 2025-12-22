class CommandRateLimiter:
    """Rate limiter for OVMS commands.

    Prevents sending too many commands in a short period to avoid overwhelming the OVMS module.
    """

    def __init__(self, max_calls: int = 5, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def can_call(self) -> bool:
        import time
        now = time.time()
        # Remove calls outside the period window
        self.calls = [call_time for call_time in self.calls if now - call_time < self.period]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

    def calls_remaining(self) -> int:
        import time
        now = time.time()
        # Remove calls outside the period window
        self.calls = [call_time for call_time in self.calls if now - call_time < self.period]
        return max(0, self.max_calls - len(self.calls))

    def time_to_next_call(self) -> float:
        import time
        now = time.time()
        # Remove calls outside the period window
        self.calls = [call_time for call_time in self.calls if now - call_time < self.period]
        
        if len(self.calls) < self.max_calls:
            return 0.0
        
        # Return time until the oldest call expires
        oldest_call = min(self.calls)
        time_until_expiry = self.period - (now - oldest_call)
        return max(0.0, time_until_expiry)