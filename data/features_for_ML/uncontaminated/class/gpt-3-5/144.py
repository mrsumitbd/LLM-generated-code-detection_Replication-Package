class CacheRecord:
    """A class that represents a model in the model cache."""

    def __init__(self):
        self._locked = False

    def lock(self) -> None:
        self._locked = True

    def unlock(self) -> None:
        self._locked = False

    @property
    def is_locked(self) -> bool:
        return self._locked