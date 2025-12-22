from typing import Dict, Any, Optional
import time

class ResponseCache:
    """Simple TTL-based cache for API responses."""

    def __init__(self):
        self._cache: Dict[str, tuple[Any, float]] = {}
        self._ttl_config: Dict[str, int] = {
            'default': 300,
            'users': 600,
            'posts': 300,
            'comments': 300,
        }
        self._stats: Dict[str, int] = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
        }

    def _get_cache_key(self, endpoint: str) -> str:
        return f"cache:{endpoint}"

    def _get_ttl_for_endpoint(self, endpoint: str) -> int:
        for key, ttl in self._ttl_config.items():
            if key in endpoint:
                return ttl
        return self._ttl_config['default']

    def get(self, endpoint: str) -> Optional[Any]:
        cache_key = self._get_cache_key(endpoint)
        
        if cache_key in self._cache:
            value, timestamp = self._cache[cache_key]
            ttl = self._get_ttl_for_endpoint(endpoint)
            
            if time.time() - timestamp < ttl:
                self._stats['hits'] += 1
                return value
            else:
                del self._cache[cache_key]
        
        self._stats['misses'] += 1
        return None

    def set(self, endpoint: str, value: Any) -> None:
        cache_key = self._get_cache_key(endpoint)
        self._cache[cache_key] = (value, time.time())
        self._stats['sets'] += 1

    def clear(self, endpoint: Optional[str] = None) -> None:
        if endpoint is None:
            self._cache.clear()
        else:
            cache_key = self._get_cache_key(endpoint)
            if cache_key in self._cache:
                del self._cache[cache_key]

    def get_stats(self) -> Dict[str, Any]:
        total_requests = self._stats['hits'] + self._stats['misses']
        hit_rate = (self._stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hits': self._stats['hits'],
            'misses': self._stats['misses'],
            'sets': self._stats['sets'],
            'cached_items': len(self._cache),
            'hit_rate': round(hit_rate, 2),
        }