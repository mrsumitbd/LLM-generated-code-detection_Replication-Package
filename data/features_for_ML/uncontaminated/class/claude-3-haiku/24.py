import threading

class ChainCache:
    def __init__(self) -> None:
        self._cache = {}
        self._lock = threading.Lock()
        self._lock_keys = set()

    @property
    def _lock_keys(self) -> set[str]:
        return self._lock_keys

    def get(self, chain_id: str) -> tuple[str | None, float] | None:
        with self._lock:
            if chain_id in self._lock_keys:
                return None
            self._lock_keys.add(chain_id)

        if chain_id in self._cache:
            value, timestamp = self._cache[chain_id]
            with self._lock:
                self._lock_keys.remove(chain_id)
            return value, timestamp
        else:
            with self._lock:
                self._lock_keys.remove(chain_id)
            return None, 0.0