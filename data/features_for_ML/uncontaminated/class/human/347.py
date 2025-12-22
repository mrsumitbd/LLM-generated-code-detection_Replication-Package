
class CircuitBreakerConfig:
    """Circuit breaker configuration."""
    failure_threshold: int = 5
    recovery_timeout: int = 60  # seconds
    test_request_timeout: int = 10  # seconds
    success_threshold: int = 2  # consecutive successes to close