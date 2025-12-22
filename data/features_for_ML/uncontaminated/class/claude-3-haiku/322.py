from typing import Dict, Any
from datetime import datetime, timedelta

class ResponseCache:
    """Simple TTL-based cache for API responses."""

    def __init__(self):
        self.cache = {}
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }

    def _get_cache_key(self, endpoint: str) -> str:
        return f"response_{endpoint}"

    def _get_ttl_for_endpoint(self, endpoint: str) -> int:
        # Implement your own logic to determine the TTL for each endpoint
        return 60  # Default TTL of 60 seconds

    def get(self, endpoint: str) -> Dict[str, Any]:
        cache_key = self._get_cache_key(endpoint)
        if cache_key in self.cache:
            cached_response, expiration_time = self.cache[cache_key]
            if datetime.now() < expiration_time:
                self.stats["hits"] += 1
                return cached_response
            else:
                del self.cache[cache_key]
                self.stats["evictions"] += 1

        self.stats["misses"] += 1
        return {}

    def set(self, endpoint: str, response: Dict[str, Any]) -> None:
        cache_key = self._get_cache_key(endpoint)
        ttl = self._get_ttl_for_endpoint(endpoint)
        expiration_time = datetime.now() + timedelta(seconds=ttl)
        self.cache[cache_key] = (response, expiration_time)

    def get_stats(self) -> Dict[str, Any]:
        return self.stats