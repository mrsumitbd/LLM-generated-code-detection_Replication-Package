from typing import Optional, Any, Dict
import time
import threading

class DeploymentStatusCache:
    """
    A simple, thread-safe, in-memory, time-based cache.
    """

    def __init__(self, default_ttl: int = 300):
        self.cache = {}
        self.default_ttl = default_ttl
        self.lock = threading.Lock()

    def get(self, domain: str) -> Optional[Any]:
        with self.lock:
            if domain in self.cache:
                return self.cache[domain]['result']
            return None

    def set(self, domain: str, result: Any, ttl: Optional[int] = None) -> None:
        with self.lock:
            self.cache[domain] = {
                'result': result,
                'expiry_time': time.time() + (ttl if ttl is not None else self.default_ttl)
            }

    def clear(self) -> int:
        with self.lock:
            size = len(self.cache)
            self.cache.clear()
            return size

    def _clean_expired(self) -> None:
        with self.lock:
            current_time = time.time()
            self.cache = {domain: data for domain, data in self.cache.items() if data['expiry_time'] > current_time}

    def get_stats(self) -> Dict[str, Any]:
        with self.lock:
            return {
                'cache_size': len(self.cache),
                'default_ttl': self.default_ttl
            }

    def set_ttl(self, ttl: int) -> bool:
        with self.lock:
            if ttl > 0:
                self.default_ttl = ttl
                return True
            return False