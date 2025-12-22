from typing import Dict, Any

class BuildConfiguration:
    """Configuration for a PCILeech firmware build."""

    def __init__(self, is_advanced: bool):
        self.is_advanced = is_advanced

    @property
    def is_advanced(self) -> bool:
        return self._is_advanced

    def to_dict(self) -> Dict[str, Any]:
        return {"is_advanced": self.is_advanced}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BuildConfiguration":
        return cls(data["is_advanced"])