import threading
import time
from typing import Any, Dict, List, Optional, Tuple

class DeploymentStatusCache:
    """
    A simple, thread-safe, in-memory, time-based cache.
    """
    def __init__(self, default_ttl: int = 300):
        self._cache: Dict[str, _CacheEntry] = {}
        self._default_ttl: int = default_ttl
        self._lock = threading.Lock()

    def get(self, domain: str) -> Optional[Any]:
        """Get a cached result for a domain, returning None if expired or not found."""
        with self._lock:
            entry = self._cache.get(domain)
            if entry and time.time() <= entry.expires_at:
                return entry.result
        return None
        
    def set(self, domain: str, result: Any, ttl: Optional[int] = None) -> None:
        """Cache a result for a domain with a specific or default TTL."""
        effective_ttl = ttl if ttl is not None else self._default_ttl
        entry = _CacheEntry(
            result=result,
            timestamp=time.time(),
            expires_at=time.time() + effective_ttl,
            ttl=effective_ttl
        )
        with self._lock:
            self._cache[domain] = entry
        
    def clear(self) -> int:
        """Clear all entries from the cache, returning the number of cleared items."""
        with self._lock:
            cleared_count = len(self._cache)
            self._cache.clear()
        return cleared_count
    
    def _clean_expired(self) -> None:
        """Internal method to remove all expired entries. Assumes lock is already held."""
        current_time = time.time()
        expired_keys = [k for k, v in self._cache.items() if current_time > v.expires_at]
        for key in expired_keys:
            del self._cache[key]
        
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the cache's current state, cleaning expired entries first."""
        with self._lock:
            self._clean_expired()
            entries = []
            current_time = time.time()
            for domain, entry in self._cache.items():
                deployed = False
                if isinstance(entry.result, dict):
                    deployed = bool(entry.result.get('deployed', False))
                entries.append({
                    'domain': domain,
                    'age': int(current_time - entry.timestamp),
                    'remaining': int(entry.expires_at - current_time),
                    'status': 'deployed' if deployed else 'not-deployed'
                })
            
            return {
                'total_entries': len(self._cache),
                'current_ttl': self._default_ttl,
                'entries': sorted(entries, key=lambda x: x['domain'])
            }
        
    def set_ttl(self, ttl: int) -> bool:
        """Set the default TTL for new cache entries."""
        if isinstance(ttl, (int, float)) and 30 <= ttl <= 3600:
            with self._lock:
                self._default_ttl = int(ttl)
            return True
        return False