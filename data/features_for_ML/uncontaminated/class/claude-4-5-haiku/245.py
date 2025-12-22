class OpenAIResourceWithRawResponse:

    def __init__(self, openai: OpenAIResource) -> None:
        self._openai = openai

    @cached_property
    def keys(self) -> KeysResourceWithRawResponse:
        return KeysResourceWithRawResponse(self._openai.keys)