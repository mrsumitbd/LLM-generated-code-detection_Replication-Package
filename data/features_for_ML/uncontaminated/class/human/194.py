from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
)

class _EMPTY_DATA_TYPE:
    """A special type to represent empty data."""

    def __init__(self, name: str = "EMPTY_DATA"):
        self.name = name

    def __bool__(self):
        return False

    def __str__(self):
        return f"EmptyData({self.name})"

    def is_same(self, obj: Any) -> bool:
        """Check if the object is the same as the current object.

        Args:
            obj (Any): The object to compare with.

        Returns:
            bool: True if the object is the same as the current object, False otherwise.
        """
        if not isinstance(obj, _EMPTY_DATA_TYPE):
            return False
        return self == obj