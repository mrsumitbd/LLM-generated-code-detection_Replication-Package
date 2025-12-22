import threading
import time
from typing import Optional, Any, Dict


class DeploymentStatusCache:
    """
    A simple, thread-safe, in-memory, time-based cache.
    """

    def __init__(self, default_ttl: int = 300):
        self._cache: Dict[str, tuple[Any, float]] = {}
        self._default_ttl = default_ttl
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def get(self, domain: str) -> Optional[Any]:
        with self._lock:
            self._clean_expired()
            if domain in self._cache:
                value, expiry_time = self._cache[domain]
                if expiry_time > time.time():
                    self._hits += 1
                    return value
                else:
                    del self._cache[domain]
            self._misses += 1
            return None

    def set(self, domain: str, result: Any, ttl: Optional[int] = None) -> None:
        with self._lock:
            ttl_to_use = ttl if ttl is not None else self._default_ttl
            expiry_time = time.time() + ttl_to_use
            self._cache[domain] = (result, expiry_time)

    def clear(self) -> int:
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            return count

    def _clean_expired(self) -> None:
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry_time) in self._cache.items()
            if expiry_time <= current_time
        ]
        for key in expired_keys:
            del self._cache[key]

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            self._clean_expired()
            total_requests = self._hits + self._misses
            hit_rate = (self._hits / total_requests * 100) if total_requests > 0 else 0
            return {
                "size": len(self._cache),
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
                "default_ttl": self._default_ttl
            }

    def set_ttl(self, ttl: int) -> bool:
        if ttl <= 0:
            return False
        with self._lock:
            self._default_ttl = ttl
            return True