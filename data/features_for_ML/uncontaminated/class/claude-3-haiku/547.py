class CacheEntry:
    def __init__(self, value, timestamp):
        self._value = value
        self._timestamp = timestamp

    @property
    def age(self) -> float:
        import time
        return time.time() - self._timestamp

    @property
    def value(self):
        return self._value