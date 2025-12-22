class CircuitBreakerConfig:
    """Circuit breaker configuration."""

    def __init__(self, max_failures: int, reset_timeout: int, open_window: int):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.open_window = open_window

    def __eq__(self, other):
        if not isinstance(other, CircuitBreakerConfig):
            return False
        return (
            self.max_failures == other.max_failures
            and self.reset_timeout == other.reset_timeout
            and self.open_window == other.open_window
        )

    def __hash__(self):
        return hash((self.max_failures, self.reset_timeout, self.open_window))

    def __repr__(self):
        return (
            f"CircuitBreakerConfig(max_failures={self.max_failures}, "
            f"reset_timeout={self.reset_timeout}, open_window={self.open_window})"
        )