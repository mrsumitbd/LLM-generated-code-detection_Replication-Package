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

    def __init__(
        self,
        source,
        type,
        correlation_id,
        data,
        metadata=None,
    ):
        """Initialize an EmittedEvent.

        Args:
            source (EventSource): The source of the event.
            type (EventType): The type of the event.
            correlation_id (str): Unique identifier for the event stream.
            data (Union[MessageEventData, StatusEventData, ToolEventData]): The event data.
            metadata (Optional[Mapping[str, JSONSerializable]]): Additional metadata.
        """
        self.source = source
        self.type = type
        self.correlation_id = correlation_id
        self.data = data
        self.metadata = metadata

    def __repr__(self):
        return (
            f"EmittedEvent(source={self.source!r}, type={self.type!r}, "
            f"correlation_id={self.correlation_id!r}, data={self.data!r}, "
            f"metadata={self.metadata!r})"
        )

    def __eq__(self, other):
        if not isinstance(other, EmittedEvent):
            return NotImplemented
        return (
            self.source == other.source
            and self.type == other.type
            and self.correlation_id == other.correlation_id
            and self.data == other.data
            and self.metadata == other.metadata
        )

    def __hash__(self):
        return hash(
            (
                self.source,
                self.type,
                self.correlation_id,
                self.data,
                self.metadata,
            )
        )