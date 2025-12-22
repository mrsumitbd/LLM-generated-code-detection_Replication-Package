from typing import Any

# Assume RetryConfigs is defined elsewhere and imported into this module.
# If it is not imported, the following import will fail and the caller
# should provide the correct import path.
try:
    from .retry_configs import RetryConfigs  # type: ignore
except Exception:
    # Fallback: define a minimal RetryConfigs dataclass for demonstration.
    from dataclasses import dataclass

    @dataclass
    class RetryConfigs:
        max_attempts: int = 3
        backoff_factor: float = 1.0
        status_forcelist: Any = None
        method_whitelist: Any = None

def get_global_config_retries() -> RetryConfigs:
    """
    Retrieve the global retry configuration.

    This function attempts to fetch retry settings from a global configuration
    source. If no configuration is found, it returns a RetryConfigs instance
    with default values.

    Returns:
        RetryConfigs: The retry configuration object.
    """
    # Attempt to import a global configuration dictionary if available.
    try:
        from .config import global_config  # type: ignore
    except Exception:
        global_config = {}

    # Extract the retry configuration section.
    retry_cfg = global_config.get("retries", {})

    # Ensure the configuration is a mapping; otherwise, use defaults.
    if not isinstance(retry_cfg, dict):
        retry_cfg = {}

    # Construct and return the RetryConfigs instance.
    return RetryConfigs(**retry_cfg)