def get_global_config_retries() -> RetryConfigs:
    """Get the global retry configuration."""
    return _global_config.retries