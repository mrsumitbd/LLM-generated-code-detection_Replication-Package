class CacheRecord:
    """A class that represents a model in the model cache."""

    def __init__(self) -> None:
        self._lock_count = 0

    def lock(self) -> None:
        self._lock_count += 1

    def unlock(self) -> None:
        if self._lock_count > 0:
            self._lock_count -= 1

    @property
    def is_locked(self) -> bool:
        return self._lock_count > 0