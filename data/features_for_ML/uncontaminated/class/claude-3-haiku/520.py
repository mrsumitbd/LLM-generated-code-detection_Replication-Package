import time
from typing import Any, Dict, Optional

class DeploymentStatusCache:
    """
    A simple, thread-safe, in-memory, time-based cache.
    """

    def __init__(self, default_ttl: int = 300):
        self.cache = {}
        self.default_ttl = default_ttl
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_items": 0,
            "current_items": 0
        }

    def get(self, domain: str) -> Optional[Any]:
        if domain in self.cache:
            if self.cache[domain]["expiration"] > time.time():
                self.stats["hits"] += 1
                return self.cache[domain]["result"]
            else:
                del self.cache[domain]
                self.stats["misses"] += 1
                return None
        else:
            self.stats["misses"] += 1
            return None

    def set(self, domain: str, result: Any, ttl: Optional[int] = None) -> None:
        if ttl is None:
            ttl = self.default_ttl
        self.cache[domain] = {
            "result": result,
            "expiration": time.time() + ttl
        }
        self.stats["total_items"] += 1
        self.stats["current_items"] += 1

    def clear(self) -> int:
        evicted = self.stats["current_items"]
        self.cache.clear()
        self.stats["current_items"] = 0
        self.stats["evictions"] += evicted
        return evicted

    def _clean_expired(self) -> None:
        now = time.time()
        for domain, entry in list(self.cache.items()):
            if entry["expiration"] <= now:
                del self.cache[domain]
                self.stats["current_items"] -= 1
                self.stats["evictions"] += 1

    def get_stats(self) -> Dict[str, Any]:
        self._clean_expired()
        return self.stats

    def set_ttl(self, ttl: int) -> bool:
        if ttl <= 0:
            return False
        self.default_ttl = ttl
        return True