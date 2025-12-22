class OpenAIResourceWithStreamingResponse:

    def __init__(self, openai: OpenAIResource) -> None:
        self._openai = openai

    @cached_property
    def keys(self) -> KeysResourceWithStreamingResponse:
        return KeysResourceWithStreamingResponse(self._openai.keys)