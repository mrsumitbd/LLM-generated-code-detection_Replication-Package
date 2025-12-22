from typing import Dict, Any

class BehavioralRegister:
    """Definition of a behavioral register."""

    def __init__(self):
        self._data: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return self._data.copy()

    def register(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def clear(self) -> None:
        self._data.clear()

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __repr__(self) -> str:
        return f"BehavioralRegister({self._data})"