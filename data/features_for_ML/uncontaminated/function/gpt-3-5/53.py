def get_isolation_provider() -> Callable:
    def isolation_provider() -> str:
        return "SparkIsolationContext"

    return isolation_provider