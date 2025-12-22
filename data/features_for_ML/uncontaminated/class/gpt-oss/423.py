import json
from collections.abc import Iterable
from typing import Any, Dict, List, Optional, Union


class MarketIntelligence:
    """Container for comprehensive market intelligence."""

    def __init__(self, name: str = "Unnamed Market", data: Optional[Dict[str, Any]] = None):
        self.name: str = name
        self._data: Dict[str, Any] = dict(data) if data else {}

    # Basic data manipulation
    def add_entry(self, key: str, value: Any) -> None:
        """Add or update a market intelligence entry."""
        self._data[key] = value

    def get_entry(self, key: str) -> Any:
        """Retrieve an entry by key."""
        return self._data[key]

    def remove_entry(self, key: str) -> None:
        """Remove an entry by key."""
        self._data.pop(key, None)

    def list_entries(self) -> List[str]:
        """Return a list of all entry keys."""
        return list(self._data.keys())

    # Convenience methods
    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        self.remove_entry(key)

    # Representation
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, entries={len(self._data)})"

    def __str__(self) -> str:
        return f"{self.name} Market Intelligence ({len(self._data)} entries)"

    # Serialization
    def to_json(self, indent: Optional[int] = None) -> str:
        """Serialize the market intelligence to a JSON string."""
        payload = {"name": self.name, "data": self._data}
        return json.dumps(payload, indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "MarketIntelligence":
        """Create a MarketIntelligence instance from a JSON string."""
        payload = json.loads(json_str)
        return cls(name=payload.get("name", "Unnamed Market"), data=payload.get("data", {}))

    # Analysis helpers
    def analyze_trends(self, key: str) -> Optional[float]:
        """
        If the entry associated with `key` is an iterable of numeric values,
        return the average; otherwise return None.
        """
        value = self._data.get(key)
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            numeric = [v for v in value if isinstance(v, (int, float))]
            if numeric:
                return sum(numeric) / len(numeric)
        return None

    def merge(self, other: "MarketIntelligence") -> None:
        """Merge another MarketIntelligence into this one, overwriting duplicates."""
        self._data.update(other._data)

    # Utility
    def clear(self) -> None:
        """Clear all entries."""
        self._data.clear()