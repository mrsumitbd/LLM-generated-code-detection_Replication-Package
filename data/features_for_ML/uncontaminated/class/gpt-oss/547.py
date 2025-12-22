import time
from typing import Any


class CacheEntry:
    """
    A simple cache entry that stores a value and the time it was created.
    The `age` property returns the elapsed time in seconds since the entry
    was created.
    """

    def __init__(self, value: Any, timestamp: float | None = None) -> None:
        """
        Initialize a new CacheEntry.

        :param value: The value to cache.
        :param timestamp: Optional creation timestamp. If omitted, the current
                          time is used.
        """
        self.value = value
        self._timestamp = timestamp if timestamp is not None else time.time()

    @property
    def age(self) -> float:
        """
        Return the age of the cache entry in seconds.

        :return: Time elapsed since the entry was created.
        """
        return time.time() - self._timestamp

    def __repr__(self) -> str:
        return f"<CacheEntry value={self.value!r} age={self.age:.2f}s>"