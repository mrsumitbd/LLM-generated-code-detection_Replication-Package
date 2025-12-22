from functools import cached_property

class OpenAIResourceWithStreamingResponse:

    def __init__(self, openai: OpenAIResource) -> None:
        pass

    @cached_property
    def keys(self) -> KeysResourceWithStreamingResponse:
        pass