class RateLimiter:
    """Convenience class for enforcing rates in loops."""

    def __init__(self, hz):
        self.interval = 1.0 / hz
        self.last_time = 0

    def sleep(self, env):
        current_time = env.now
        elapsed_time = current_time - self.last_time
        if elapsed_time < self.interval:
            sleep_time = self.interval - elapsed_time
            env.timeout(sleep_time)
        self.last_time = env.now