from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class BuildConfiguration:
    """
    Configuration for a PCILeech firmware build.

    Attributes
    ----------
    target : str
        Target platform or device name.
    compiler : str
        Compiler to use (e.g., "gcc", "clang").
    flags : List[str]
        List of compiler flags.
    advanced_options : Optional[Dict[str, Any]]
        Dictionary of advanced build options. If set, the configuration is considered advanced.
    """

    target: str = "default"
    compiler: str = "gcc"
    flags: List[str] = field(default_factory=list)
    advanced_options: Optional[Dict[str, Any]] = None

    @property
    def is_advanced(self) -> bool:
        """Return True if advanced options are specified."""
        return bool(self.advanced_options)

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the configuration."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BuildConfiguration":
        """Create a BuildConfiguration instance from a dictionary."""
        # Ensure that missing keys get default values
        return cls(
            target=data.get("target", "default"),
            compiler=data.get("compiler", "gcc"),
            flags=data.get("flags", []),
            advanced_options=data.get("advanced_options"),
        )