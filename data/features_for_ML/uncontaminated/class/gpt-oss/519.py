from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass(order=True, frozen=True)
class AstraYaoChordManagerTriggerRecord:
    """
    A lightweight immutable record representing a trigger event in the
    Astra Yao Chord Manager system.

    Attributes
    ----------
    trigger_id : str
        Unique identifier for the trigger. Generated automatically if not
        provided.
    event_type : str
        Human‑readable type of the event (e.g. "CHORD_START", "CHORD_END").
    payload : Dict[str, Any]
        Arbitrary JSON‑serialisable data associated with the trigger.
    timestamp : datetime
        UTC timestamp when the record was created. Defaults to ``datetime.now``.
    status : str
        Current status of the trigger (e.g. "PENDING", "PROCESSED").
    metadata : Dict[str, Any]
        Optional key/value pairs for additional context.
    """

    trigger_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = field(default="UNKNOWN")
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = field(default="PENDING")
    metadata: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AstraYaoChordManagerTriggerRecord":
        """Create a record from a plain dictionary."""
        data = data.copy()
        # Convert timestamp if string
        ts = data.get("timestamp")
        if isinstance(ts, str):
            data["timestamp"] = datetime.fromisoformat(ts)
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "AstraYaoChordManagerTriggerRecord":
        """Create a record from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dictionary representation."""
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d

    def to_json(self, *, indent: Optional[int] = None) -> str:
        """Return a JSON string representation."""
        return json.dumps(self.to_dict(), indent=indent)

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def age(self, *, now: Optional[datetime] = None) -> float:
        """Return age in seconds relative to ``now`` (defaults to UTC now)."""
        now = now or datetime.now(timezone.utc)
        return (now - self.timestamp).total_seconds()

    def is_active(self) -> bool:
        """Return True if status is not terminal."""
        return self.status not in {"PROCESSED", "FAILED", "CANCELLED"}

    def with_status(self, new_status: str) -> "AstraYaoChordManagerTriggerRecord":
        """Return a new record with updated status."""
        return self.__class__(
            trigger_id=self.trigger_id,
            event_type=self.event_type,
            payload=self.payload,
            timestamp=self.timestamp,
            status=new_status,
            metadata=self.metadata,
        )

    def with_payload(self, new_payload: Dict[str, Any]) -> "AstraYaoChordManagerTriggerRecord":
        """Return a new record with updated payload."""
        return self.__class__(
            trigger_id=self.trigger_id,
            event_type=self.event_type,
            payload=new_payload,
            timestamp=self.timestamp,
            status=self.status,
            metadata=self.metadata,
        )

    def with_metadata(self, key: str, value: Any) -> "AstraYaoChordManagerTriggerRecord":
        """Return a new record with an added/updated metadata entry."""
        new_meta = dict(self.metadata)
        new_meta[key] = value
        return self.__class__(
            trigger_id=self.trigger_id,
            event_type=self.event_type,
            payload=self.payload,
            timestamp=self.timestamp,
            status=self.status,
            metadata=new_meta,
        )

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"trigger_id={self.trigger_id!r}, "
            f"event_type={self.event_type!r}, "
            f"status={self.status!r}, "
            f"timestamp={self.timestamp.isoformat()!r})"
        )

    def __str__(self) -> str:
        return f"{self.event_type} ({self.trigger_id}) at {self.timestamp.isoformat()}"

    # ------------------------------------------------------------------
    # Equality and hashing are provided by dataclass (frozen=True)
    # ------------------------------------------------------------------