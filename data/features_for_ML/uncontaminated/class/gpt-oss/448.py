from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass
class BehavioralRegister:
    """Definition of a behavioral register."""

    name: str
    value: int = 0
    width: int = 32
    description: Optional[str] = None
    reset_value: Optional[int] = None
    access: str = "rw"  # read/write, read-only, write-only

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the register."""
        return asdict(self)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name!r}, value={self.value!r}, "
            f"width={self.width!r}, description={self.description!r}, "
            f"reset_value={self.reset_value!r}, access={self.access!r})"
        )