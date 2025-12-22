from typing import Dict, Any

class ClientCapability:
    """Represents client capabilities."""

    def __init__(self, name: str, version: str, is_enabled: bool = True):
        self.name = name
        self.version = version
        self.is_enabled = is_enabled

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "is_enabled": self.is_enabled
        }