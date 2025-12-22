from datetime import datetime
from typing import Any, Dict, Optional


class YuzuhaCinema4QuickAssistTriggerRecord:
    """
    A flexible record for Yuzuha Cinema 4 Quick Assist triggers.
    Stores core trigger information and allows arbitrary extra fields.
    """

    def __init__(
        self,
        trigger_id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        active: bool = True,
        timestamp: Optional[datetime] = None,
        **extra: Any,
    ) -> None:
        self.trigger_id = trigger_id
        self.name = name
        self.description = description
        self.active = active
        self.timestamp = timestamp or datetime.utcnow()
        self.extra = dict(extra)

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the record."""
        data: Dict[str, Any] = {
            "trigger_id": self.trigger_id,
            "name": self.name,
            "description": self.description,
            "active": self.active,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
        data.update(self.extra)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "YuzuhaCinema4QuickAssistTriggerRecord":
        """Create a record instance from a dictionary."""
        timestamp = data.get("timestamp")
        if timestamp:
            timestamp = datetime.fromisoformat(timestamp)
        extra = {
            k: v
            for k, v in data.items()
            if k not in {"trigger_id", "name", "description", "active", "timestamp"}
        }
        return cls(
            trigger_id=data.get("trigger_id"),
            name=data.get("name"),
            description=data.get("description"),
            active=data.get("active", True),
            timestamp=timestamp,
            **extra,
        )

    def __repr__(self) -> str:
        return (
            f"<YuzuhaCinema4QuickAssistTriggerRecord "
            f"id={self.trigger_id!r} name={self.name!r} active={self.active}>"
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, YuzuhaCinema4QuickAssistTriggerRecord):
            return False
        return self.to_dict() == other.to_dict()