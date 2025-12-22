import time
from dataclasses import dataclass, field
from typing import Literal, Mapping, Optional, TypedDict, Union
from flux0_core.sessions import (
    EventId,
    EventSource,
    EventType,
    MessageEventData,
    StatusEventData,
    ToolEventData,
)
from flux0_core.types import JSONSerializable

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

    id: EventId
    source: EventSource
    type: EventType
    correlation_id: str
    data: Union[MessageEventData, StatusEventData, ToolEventData]
    metadata: Optional[Mapping[str, JSONSerializable]] = None
    timestamp: float = field(default_factory=time.time)