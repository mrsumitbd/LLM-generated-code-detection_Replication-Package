from typing import NamedTuple

class RetryConfigs(NamedTuple):
    max_retries: int
    backoff_factor: float

def get_global_config_retries() -> RetryConfigs:
    return RetryConfigs(max_retries=3, backoff_factor=0.5)