from typing import Generator, Union

# Assume these classes are defined elsewhere in the codebase
# from some_module import DTMFLookAheadCharacterBuffer, AgentResponse, DTMFOutputEvent

class DTMFLookAheadStringBuffer:
    """
    Wrapper ontop of DTMFLookAheadCharacterBuffer, but will yield strings instead of characters
    """

    def __init__(self):
        # Instantiate the underlying character buffer
        self._char_buffer = DTMFLookAheadCharacterBuffer()
        # Buffer to accumulate characters into a string
        self._current_string = ""

    def feed(self, string: str) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        """
        Feed a string into the underlying character buffer and yield events.
        Accumulate characters into a string until an AgentResponse is encountered,
        at which point the accumulated string is yielded.
        """
        for event in self._char_buffer.feed(string):
            if isinstance(event, DTMFOutputEvent):
                # Append the character represented by the DTMF event to the buffer
                # Assuming the event has an attribute `digit` that holds the character
                self._current_string += getattr(event, "digit", "")
                # Yield the original event unchanged
                yield event
            elif isinstance(event, AgentResponse):
                # When an AgentResponse is encountered, flush the accumulated string
                if self._current_string:
                    yield self._current_string
                    self._current_string = ""
                # Yield the AgentResponse unchanged
                yield event
            else:
                # In case of unexpected event types, just pass them through
                yield event

    def flush(self) -> Generator[Union[AgentResponse, DTMFOutputEvent], None, None]:
        """
        Flush the underlying character buffer and yield any remaining accumulated string.
        """
        for event in self._char_buffer.flush():
            if isinstance(event, DTMFOutputEvent):
                self._current_string += getattr(event, "digit", "")
                yield event
            elif isinstance(event, AgentResponse):
                if self._current_string:
                    yield self._current_string
                    self._current_string = ""
                yield event
            else:
                yield event

        # After flushing the underlying buffer, if there's any remaining string, yield it
        if self._current_string:
            yield self._current_string
            self._current_string = ""