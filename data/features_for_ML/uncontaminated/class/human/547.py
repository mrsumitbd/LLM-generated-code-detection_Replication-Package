import time
from typing import Any, Dict, Optional, Callable

class CacheEntry:
    data: Any
    timestamp: float
    endpoint: str
    ttl: int

    @property
    def age(self) -> float:
        return time.time() - self.timestamp