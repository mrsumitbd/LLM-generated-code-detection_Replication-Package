from typing import Dict, Any

class BuildConfiguration:
    """Configuration for a PCILeech firmware build."""

    def __init__(self, is_advanced: bool, target_platform: str, target_architecture: str, target_version: str, target_revision: str):
        self._is_advanced = is_advanced
        self._target_platform = target_platform
        self._target_architecture = target_architecture
        self._target_version = target_version
        self._target_revision = target_revision

    @property
    def is_advanced(self) -> bool:
        return self._is_advanced

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_advanced": self._is_advanced,
            "target_platform": self._target_platform,
            "target_architecture": self._target_architecture,
            "target_version": self._target_version,
            "target_revision": self._target_revision
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BuildConfiguration":
        return cls(
            is_advanced=data["is_advanced"],
            target_platform=data["target_platform"],
            target_architecture=data["target_architecture"],
            target_version=data["target_version"],
            target_revision=data["target_revision"]
        )