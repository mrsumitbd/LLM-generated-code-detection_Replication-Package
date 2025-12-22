class ChainCache:
    
    def __init__(self) -> None:
        self._cache = {}
        self._lock_keys = set()

    @property
    def _lock_keys(self) -> set[str]:
        return self._lock_keys

    def get(self, chain_id: str) -> tuple[str | None, float] | None:
        if chain_id in self._cache:
            return self._cache[chain_id]
        return None