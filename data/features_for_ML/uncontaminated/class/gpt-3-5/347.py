class CircuitBreakerConfig:
    def __init__(self, failure_threshold, recovery_timeout):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

    def __str__(self):
        return f"CircuitBreakerConfig(failure_threshold={self.failure_threshold}, recovery_timeout={self.recovery_timeout})"