class CircuitBreakerConfig:
    """Circuit breaker configuration."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception,
        name: str = None
    ):
        """Initialize CircuitBreakerConfig.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exception: Exception type to catch
            name: Name of the circuit breaker
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.name = name or "CircuitBreaker"
    
    def __repr__(self) -> str:
        return (
            f"CircuitBreakerConfig(failure_threshold={self.failure_threshold}, "
            f"recovery_timeout={self.recovery_timeout}, "
            f"expected_exception={self.expected_exception.__name__}, "
            f"name={self.name})"
        )