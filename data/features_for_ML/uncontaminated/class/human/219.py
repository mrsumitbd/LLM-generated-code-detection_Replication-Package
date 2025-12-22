from collections.abc import Generator
from line.events import AgentResponse, DTMFOutputEvent
from typing import Union

class DTMFLookAheadStringBuffer:
    """
    Wrapper ontop of DTMFLookAheadCharacterBuffer, but will yield strings instead of characters
    """

    def __init__(self):
        self.buffer = DTMFLookAheadCharacterBuffer()

    def feed(self, string: str) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        for char in string:
            for item in self.buffer.feed(char):
                if isinstance(item, DTMFOutputEvent):
                    for digit in item.button:
                        yield DTMFOutputEvent(button=digit)
                else:
                    yield item

    def flush(self) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        for item in self.buffer.flush():
            if isinstance(item, DTMFOutputEvent):
                for digit in split_dtmf_output(item):
                    yield digit
            else:
                yield item