from typing import Dict, Any

class ClientCapability:
    """Represents client capabilities."""

    def __init__(self):
        self._capabilities: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return self._capabilities.copy()

    def add_capability(self, name: str, value: Any) -> None:
        self._capabilities[name] = value

    def get_capability(self, name: str) -> Any:
        return self._capabilities.get(name)

    def has_capability(self, name: str) -> bool:
        return name in self._capabilities

    def remove_capability(self, name: str) -> None:
        if name in self._capabilities:
            del self._capabilities[name]

    def clear_capabilities(self) -> None:
        self._capabilities.clear()

    def __repr__(self) -> str:
        return f"ClientCapability({self._capabilities})"