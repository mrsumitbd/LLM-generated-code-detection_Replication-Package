from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class VivianDotTriggerRecord:
    """
    A lightweight record representing a trigger event in the VivianDot system.
    """
    trigger_id: Optional[str] = None
    trigger_name: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.timestamp, str):
            try:
                self.timestamp = datetime.fromisoformat(self.timestamp)
            except ValueError:
                raise ValueError("timestamp must be a datetime or ISO‑8601 string")

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation of the record."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VivianDotTriggerRecord":
        """Create a record instance from a dictionary."""
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            data["timestamp"] = datetime.fromisoformat(timestamp)
        return cls(**data)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"trigger_id={self.trigger_id!r}, "
            f"trigger_name={self.trigger_name!r}, "
            f"timestamp={self.timestamp.isoformat()}, "
            f"payload={self.payload!r}, "
            f"metadata={self.metadata!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VivianDotTriggerRecord):
            return NotImplemented
        return (
            self.trigger_id == other.trigger_id
            and self.trigger_name == other.trigger_name
            and self.timestamp == other.timestamp
            and self.payload == other.payload
            and self.metadata == other.metadata
        )