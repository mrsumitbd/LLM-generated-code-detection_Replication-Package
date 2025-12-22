from dataclasses import dataclass
from typing import Tuple

@dataclass
class RetryConfigs:
    max_retries: int
    retry_delay_seconds: float
    backoff_factor: float

def get_global_config_retries() -> RetryConfigs:
    return RetryConfigs(
        max_retries=3,
        retry_delay_seconds=0.5,
        backoff_factor=2.0
    )