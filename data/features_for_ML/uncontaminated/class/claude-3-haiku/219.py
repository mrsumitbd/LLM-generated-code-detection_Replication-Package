from typing import Generator, Union
from .dtmf_look_ahead_character_buffer import DTMFLookAheadCharacterBuffer
from .agent_response import AgentResponse
from .dtmf_output_event import DTMFOutputEvent

class DTMFLookAheadStringBuffer:
    """
    Wrapper ontop of DTMFLookAheadCharacterBuffer, but will yield strings instead of characters
    """

    def __init__(self):
        self.buffer = DTMFLookAheadCharacterBuffer()

    def feed(self, string: str) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        for char in string:
            for event in self.buffer.feed(char):
                yield event

    def flush(self) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        for event in self.buffer.flush():
            yield event