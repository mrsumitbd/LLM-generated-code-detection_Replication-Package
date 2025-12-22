class CircuitBreakerConfig:
    """Circuit breaker configuration."""

    __slots__ = (
        "failure_threshold",
        "recovery_timeout",
        "half_open_max_successes",
        "name",
    )

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_successes: int = 3,
        name: str = "default",
    ):
        if not isinstance(failure_threshold, int) or failure_threshold <= 0:
            raise ValueError("failure_threshold must be a positive integer")
        if not isinstance(recovery_timeout, (int, float)) or recovery_timeout <= 0:
            raise ValueError("recovery_timeout must be a positive number")
        if not isinstance(half_open_max_successes, int) or half_open_max_successes <= 0:
            raise ValueError("half_open_max_successes must be a positive integer")
        if not isinstance(name, str):
            raise ValueError("name must be a string")

        self.failure_threshold = failure_threshold
        self.recovery_timeout = float(recovery_timeout)
        self.half_open_max_successes = half_open_max_successes
        self.name = name

    def to_dict(self) -> dict:
        return {
            "failure_threshold": self.failure_threshold,
            "recovery_timeout": self.recovery_timeout,
            "half_open_max_successes": self.half_open_max_successes,
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            failure_threshold=data.get("failure_threshold", 5),
            recovery_timeout=data.get("recovery_timeout", 60.0),
            half_open_max_successes=data.get("half_open_max_successes", 3),
            name=data.get("name", "default"),
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"failure_threshold={self.failure_threshold}, "
            f"recovery_timeout={self.recovery_timeout}, "
            f"half_open_max_successes={self.half_open_max_successes}, "
            f"name={self.name!r})"
        )

    def __eq__(self, other):
        if not isinstance(other, CircuitBreakerConfig):
            return NotImplemented
        return (
            self.failure_threshold == other.failure_threshold
            and self.recovery_timeout == other.recovery_timeout
            and self.half_open_max_successes == other.half_open_max_successes
            and self.name == other.name
        )