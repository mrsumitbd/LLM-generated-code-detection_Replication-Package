import threading


class CacheRecord:
    """A class that represents a model in the model cache."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._locked = False
        self._flag_lock = threading.Lock()  # protects _locked flag

    def lock(self) -> None:
        """Acquire the lock and mark the record as locked."""
        self._lock.acquire()
        with self._flag_lock:
            self._locked = True

    def unlock(self) -> None:
        """Release the lock and mark the record as unlocked."""
        with self._flag_lock:
            self._locked = False
        self._lock.release()

    @property
    def is_locked(self) -> bool:
        """Return True if the record is currently locked."""
        with self._flag_lock:
            return self._locked