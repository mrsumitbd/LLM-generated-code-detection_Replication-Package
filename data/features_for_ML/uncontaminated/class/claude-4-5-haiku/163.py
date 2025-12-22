class RateLimiter:
    """Convenience class for enforcing rates in loops."""

    def __init__(self, hz):
        self.hz = hz
        self.period = 1.0 / hz
        self.last_time = None

    def sleep(self, env):
        import time
        current_time = time.time()
        
        if self.last_time is not None:
            elapsed = current_time - self.last_time
            sleep_time = self.period - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
                self.last_time = time.time()
            else:
                self.last_time = current_time
        else:
            self.last_time = current_time