from typing import Generator, Union

class DTMFOutputEvent:
    pass

class AgentResponse:
    pass

class DTMFLookAheadCharacterBuffer:
    pass

class DTMFLookAheadStringBuffer:
    """
    Wrapper ontop of DTMFLookAheadCharacterBuffer, but will yield strings instead of characters
    """

    def __init__(self):
        self.buffer = ""

    def feed(self, string: str) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        self.buffer += string
        while len(self.buffer) >= 2:
            yield self.buffer[:2]
            self.buffer = self.buffer[2:]

    def flush(self) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        while len(self.buffer) >= 2:
            yield self.buffer[:2]
            self.buffer = self.buffer[2:]