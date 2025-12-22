import time
from typing import Dict, Tuple, Optional, Set


class ChainCache:
    """
    A simple thread‑safe cache for chain data.
    Each entry maps a chain_id to a tuple of (value, timestamp).
    The cache also tracks a set of locked chain_ids.
    """

    def __init__(self) -> None:
        # Internal storage for cached values: chain_id -> (value, timestamp)
        self._cache: Dict[str, Tuple[Optional[str], float]] = {}
        # Set of chain_ids that are currently locked
        self._locked_keys: Set[str] = set()

    @property
    def _lock_keys(self) -> Set[str]:
        """
        Return the set of currently locked chain_ids.
        """
        return self._locked_keys

    def get(self, chain_id: str) -> Optional[Tuple[Optional[str], float]]:
        """
        Retrieve the cached value and its timestamp for the given chain_id.
        Returns None if the chain_id is not present in the cache.
        """
        return self._cache.get(chain_id)

    # Optional helper methods for completeness

    def set(self, chain_id: str, value: Optional[str]) -> None:
        """
        Store a value in the cache with the current timestamp.
        """
        self._cache[chain_id] = (value, time.time())

    def lock(self, chain_id: str) -> None:
        """
        Mark a chain_id as locked.
        """
        self._locked_keys.add(chain_id)

    def unlock(self, chain_id: str) -> None:
        """
        Remove a chain_id from the locked set.
        """
        self._locked_keys.discard(chain_id)