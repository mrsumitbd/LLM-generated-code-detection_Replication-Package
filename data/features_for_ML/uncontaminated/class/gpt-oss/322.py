from typing import Any, Dict, Tuple
import time


class ResponseCache:
    """Simple TTL-based cache for API responses."""

    def __init__(self) -> None:
        # Internal cache: key -> (value, expiry_timestamp)
        self._cache: Dict[str, Tuple[Any, float]] = {}
        # Statistics
        self._stats: Dict[str, int] = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "size": 0,
        }
        # Default TTL (seconds) and per‑endpoint overrides
        self._default_ttl: int = 60
        self._endpoint_ttl: Dict[str, int] = {
            # Example overrides; can be extended as needed
            "health": 30,
            "data": 120,
        }

    def _get_cache_key(self, endpoint: str) -> str:
        """
        Return the cache key for a given endpoint.
        By default the endpoint string itself is used.
        """
        return endpoint

    def _get_ttl_for_endpoint(self, endpoint: str) -> int:
        """
        Return the TTL (in seconds) for a given endpoint.
        If the endpoint has a specific TTL configured, that value is returned;
        otherwise the default TTL is used.
        """
        return self._endpoint_ttl.get(endpoint, self._default_ttl)

    def get_stats(self) -> Dict[str, Any]:
        """
        Return a snapshot of the current cache statistics.
        The 'size' statistic is updated to reflect the current number of
        non‑expired entries in the cache.
        """
        # Clean up expired entries before reporting size
        now = time.time()
        expired_keys = [k for k, (_, exp) in self._cache.items() if exp <= now]
        for k in expired_keys:
            del self._cache[k]
            self._stats["evictions"] += 1

        self._stats["size"] = len(self._cache)
        return dict(self._stats)