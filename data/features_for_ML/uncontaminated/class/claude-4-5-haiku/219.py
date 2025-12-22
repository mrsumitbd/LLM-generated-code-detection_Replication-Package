class DTMFLookAheadStringBuffer:
    """
    Wrapper ontop of DTMFLookAheadCharacterBuffer, but will yield strings instead of characters
    """

    def __init__(self):
        self.buffer = DTMFLookAheadCharacterBuffer()

    def feed(self, string: str) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        for char in string:
            yield from self.buffer.feed(char)

    def flush(self) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        yield from self.buffer.flush()