class CacheRecord:
    """A class that represents a model in the model cache."""

    def __init__(self):
        self._is_locked = False

    def lock(self) -> None:
        self._is_locked = True

    def unlock(self) -> None:
        self._is_locked = False

    @property
    def is_locked(self) -> bool:
        return self._is_locked