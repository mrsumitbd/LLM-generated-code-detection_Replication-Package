import time
import threading
from typing import Any, Dict, Optional


class DeploymentStatusCache:
    """
    A simple, thread‑safe, in‑memory, time‑based cache.
    """

    def __init__(self, default_ttl: int = 300):
        self._default_ttl = default_ttl
        self._store: Dict[str, tuple[Any, float]] = {}
        self._lock = threading.RLock()
        # statistics
        self._hits = 0
        self._misses = 0
        self._sets = 0
        self._evictions = 0
        self._last_cleaned = 0.0

    def get(self, domain: str) -> Optional[Any]:
        with self._lock:
            self._clean_expired()
            entry = self._store.get(domain)
            if entry is None:
                self._misses += 1
                return None
            value, expire_at = entry
            if expire_at < time.time():
                # expired
                del self._store[domain]
                self._evictions += 1
                self._misses += 1
                return None
            self._hits += 1
            return value

    def set(self, domain: str, result: Any, ttl: Optional[int] = None) -> None:
        with self._lock:
            self._clean_expired()
            expire_at = time.time() + (ttl if ttl is not None else self._default_ttl)
            self._store[domain] = (result, expire_at)
            self._sets += 1

    def clear(self) -> int:
        with self._lock:
            count = len(self._store)
            self._store.clear()
            return count

    def _clean_expired(self) -> None:
        now = time.time()
        expired_keys = [k for k, (_, exp) in self._store.items() if exp < now]
        for k in expired_keys:
            del self._store[k]
            self._evictions += 1
        self._last_cleaned = now

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "size": len(self._store),
                "hits": self._hits,
                "misses": self._misses,
                "sets": self._sets,
                "evictions": self._evictions,
                "default_ttl": self._default_ttl,
                "last_cleaned": self._last_cleaned,
            }

    def set_ttl(self, ttl: int) -> bool:
        with self._lock:
            if ttl <= 0:
                return False
            self._default_ttl = ttl
            return True