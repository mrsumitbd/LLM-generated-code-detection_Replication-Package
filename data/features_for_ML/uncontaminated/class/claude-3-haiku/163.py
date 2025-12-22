import time

class RateLimiter:
    """Convenience class for enforcing rates in loops."""

    def __init__(self, hz):
        self.hz = hz
        self.last_call = 0

    def sleep(self, env):
        now = time.time()
        elapsed = now - self.last_call
        delay = 1 / self.hz - elapsed
        if delay > 0:
            env.sleep(delay)
        self.last_call = time.time()