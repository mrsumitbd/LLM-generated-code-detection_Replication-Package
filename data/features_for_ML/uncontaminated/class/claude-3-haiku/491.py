from typing import Union, Optional, Mapping
from dataclasses import dataclass
from .event_types import EventType, EventSource
from .event_data import MessageEventData, StatusEventData, ToolEventData
from .utils import JSONSerializable

@dataclass
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
    metadata: Optional[Mapping[str, JSONSerializable]] = None