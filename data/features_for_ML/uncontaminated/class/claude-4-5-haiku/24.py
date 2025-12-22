class ChainCache:
    def __init__(self) -> None:
        self._cache = {}
        self._locks = set()
        self._timestamps = {}

    @property
    def _lock_keys(self) -> set[str]:
        return self._locks.copy()

    def get(self, chain_id: str) -> tuple[str | None, float] | None:
        if chain_id not in self._cache:
            return None
        return (self._cache[chain_id], self._timestamps[chain_id])

    def set(self, chain_id: str, value: str | None, timestamp: float) -> None:
        self._cache[chain_id] = value
        self._timestamps[chain_id] = timestamp

    def lock(self, chain_id: str) -> None:
        self._locks.add(chain_id)

    def unlock(self, chain_id: str) -> None:
        self._locks.discard(chain_id)

    def clear(self) -> None:
        self._cache.clear()
        self._timestamps.clear()
        self._locks.clear()

    def is_locked(self, chain_id: str) -> bool:
        return chain_id in self._locks