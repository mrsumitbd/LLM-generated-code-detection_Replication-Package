class CacheEntry:
    def __init__(self, value, timestamp=None):
        self._value = value
        self._timestamp = timestamp if timestamp is not None else __import__('time').time()

    @property
    def age(self) -> float:
        return __import__('time').time() - self._timestamp

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val