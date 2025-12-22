from typing import Union, Optional, Mapping
from event_source import EventSource
from event_type import EventType
from event_data import MessageEventData, StatusEventData, ToolEventData
from json_serializable import JSONSerializable

class EmittedEvent:
    def __init__(self, source: EventSource, event_type: EventType, correlation_id: str, data: Union[MessageEventData, StatusEventData, ToolEventData], metadata: Optional[Mapping[str, JSONSerializable]] = None):
        self.source = source
        self.type = event_type
        self.correlation_id = correlation_id
        self.data = data
        self.metadata = metadata