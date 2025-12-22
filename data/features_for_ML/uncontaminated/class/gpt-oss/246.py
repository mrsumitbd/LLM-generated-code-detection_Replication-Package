from __future__ import annotations

import json
import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Union


@dataclass
class EventCfg:
    """
    Configuration for events.

    Attributes
    ----------
    name : str
        The name of the event.
    start : datetime.datetime
        The start datetime of the event.
    end : Optional[datetime.datetime]
        The end datetime of the event. If None, the event is considered instantaneous.
    location : Optional[str]
        The location of the event.
    participants : List[str]
        List of participant identifiers.
    description : Optional[str]
        A textual description of the event.
    tags : List[str]
        Tags for categorising the event.
    metadata : Dict[str, Any]
        Arbitrary key/value metadata.
    recurrence_rule : Optional[str]
        iCalendar RRULE string for recurring events.
    """

    name: str
    start: datetime.datetime
    end: Optional[datetime.datetime] = None
    location: Optional[str] = None
    participants: List[str] = field(default_factory=list)
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    recurrence_rule: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.start, str):
            self.start = self._parse_datetime(self.start)
        if isinstance(self.end, str):
            self.end = self._parse_datetime(self.end)

        if self.end and self.end < self.start:
            raise ValueError("Event end time cannot be before start time")

    @staticmethod
    def _parse_datetime(value: str) -> datetime.datetime:
        try:
            return datetime.datetime.fromisoformat(value)
        except ValueError as exc:
            raise ValueError(f"Invalid datetime format: {value}") from exc

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation."""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        data["start"] = self.start.isoformat()
        data["end"] = self.end.isoformat() if self.end else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventCfg":
        """Create an EventCfg instance from a dictionary."""
        data = data.copy()
        # Parse datetime strings if present
        if "start" in data and isinstance(data["start"], str):
            data["start"] = cls._parse_datetime(data["start"])
        if "end" in data and isinstance(data["end"], str):
            data["end"] = cls._parse_datetime(data["end"])
        return cls(**data)

    def to_json(self) -> str:
        """Serialize the event configuration to a JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "EventCfg":
        """Deserialize an EventCfg instance from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def add_participant(self, participant_id: str) -> None:
        """Add a participant to the event."""
        if participant_id not in self.participants:
            self.participants.append(participant_id)

    def remove_participant(self, participant_id: str) -> None:
        """Remove a participant from the event."""
        if participant_id in self.participants:
            self.participants.remove(participant_id)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the event."""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the event."""
        if tag in self.tags:
            self.tags.remove(tag)

    def is_upcoming(self, reference: Optional[datetime.datetime] = None) -> bool:
        """Return True if the event starts after the reference time."""
        ref = reference or datetime.datetime.now(tz=self.start.tzinfo)
        return self.start > ref

    def is_ongoing(self, reference: Optional[datetime.datetime] = None) -> bool:
        """Return True if the event is currently ongoing."""
        ref = reference or datetime.datetime.now(tz=self.start.tzinfo)
        if self.end:
            return self.start <= ref <= self.end
        return self.start <= ref

    def is_past(self, reference: Optional[datetime.datetime] = None) -> bool:
        """Return True if the event has already finished."""
        ref = reference or datetime.datetime.now(tz=self.start.tzinfo)
        if self.end:
            return ref > self.end
        return ref > self.start

    def duration(self) -> Optional[datetime.timedelta]:
        """Return the duration of the event, or None if instantaneous."""
        if self.end:
            return self.end - self.start
        return None

    def __repr__(self) -> str:
        return (
            f"EventCfg(name={self.name!r}, start={self.start!r}, "
            f"end={self.end!r}, location={self.location!r}, "
            f"participants={self.participants!r}, tags={self.tags!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EventCfg):
            return NotImplemented
        return self.to_dict() == other.to_dict()