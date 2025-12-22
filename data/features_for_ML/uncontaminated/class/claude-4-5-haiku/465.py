class AsyncProvidersResourceWithRawResponse:

    def __init__(self, providers: AsyncProvidersResource) -> None:
        self._providers = providers

    @cached_property
    def anthropic(self) -> AsyncAnthropicResourceWithRawResponse:
        return AsyncAnthropicResourceWithRawResponse(self._providers.anthropic)

    @cached_property
    def openai(self) -> AsyncOpenAIResourceWithRawResponse:
        return AsyncOpenAIResourceWithRawResponse(self._providers.openai)