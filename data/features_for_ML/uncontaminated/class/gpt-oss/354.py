from __future__ import annotations

from typing import Dict, Iterable, Iterator, Optional, Tuple


class RuleContext:
    """Represents context information for values referenced in conditions."""

    def __init__(self, data: Optional[Dict[str, str]] = None) -> None:
        """
        Initialize the context with an optional mapping of keys to string values.
        """
        self._data: Dict[str, str] = dict(data) if data is not None else {}

    def set(self, key: str, value: str) -> None:
        """
        Set a key/value pair in the context.
        """
        self._data[key] = value

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Retrieve a value by key, returning ``default`` if the key is missing.
        """
        return self._data.get(key, default)

    def update(self, other: Iterable[Tuple[str, str]]) -> None:
        """
        Update the context with an iterable of key/value pairs.
        """
        for k, v in other:
            self._data[k] = v

    def to_dict(self) -> Dict[str, str]:
        """
        Return a shallow copy of the context as a plain dictionary.
        """
        return dict(self._data)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"