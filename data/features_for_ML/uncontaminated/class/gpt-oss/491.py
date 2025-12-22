from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Union, Dict

# Placeholder types – replace with actual imports in your project
try:
    from your_project.event_source import EventSource
    from your_project.event_type import EventType
    from your_project.event_data import (
        MessageEventData,
        StatusEventData,
        ToolEventData,
    )
    from your_project.json_serializable import JSONSerializable
except Exception:  # pragma: no cover
    EventSource = Any
    EventType = Any
    MessageEventData = Any
    StatusEventData = Any
    ToolEventData = Any
    JSONSerializable = Any


@dataclass(frozen=True)
class EmittedEvent:
    """Represents an event emitted by a source.
    This is the final form of an event after all chunks have been processed and
    closely related to the `Event` class in core.

    Attributes:
        source (EventSource): The source of the event.
        type (EventType): The type of the event.
        correlation_id (str): Unique identifier for the event stream.
        data (Union[MessageEventData, StatusEventData, ToolEventData]): The event data.
        metadata (Optional[Mapping[str, JSONSerializable]]): Additional metadata.
    """

    source: EventSource
    type: EventType
    correlation_id: str
    data: Union[MessageEventData, StatusEventData, ToolEventData]
    metadata: Optional[Mapping[str, JSONSerializable]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.correlation_id, str):
            raise TypeError("correlation_id must be a str")
        if self.metadata is not None and not isinstance(self.metadata, Mapping):
            raise TypeError("metadata must be a Mapping or None")

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON‑serialisable dictionary representation of the event."""
        return {
            "source": self.source,
            "type": self.type,
            "correlation_id": self.correlation_id,
            "data": self.data,
            "metadata": dict(self.metadata) if self.metadata else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmittedEvent":
        """Create an EmittedEvent instance from a dictionary."""
        return cls(
            source=data["source"],
            type=data["type"],
            correlation_id=data["correlation_id"],
            data=data["data"],
            metadata=data.get("metadata"),
        )