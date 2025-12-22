from typing import Any

class _EMPTY_DATA_TYPE:
    """A special type to represent empty data."""

    def __init__(self, name: str = "EMPTY_DATA"):
        self.name = name

    def __bool__(self):
        return False

    def __str__(self):
        return self.name

    def is_same(self, obj: Any) -> bool:
        return isinstance(obj, _EMPTY_DATA_TYPE) and obj.name == self.name