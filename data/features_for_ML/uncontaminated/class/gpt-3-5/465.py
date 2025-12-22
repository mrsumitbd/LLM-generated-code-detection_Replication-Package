from functools import cached_property

class AsyncProvidersResourceWithRawResponse:

    def __init__(self, providers: AsyncProvidersResource) -> None:
        self.providers = providers

    @cached_property
    def anthropic(self) -> AsyncAnthropicResourceWithRawResponse:
        return AsyncAnthropicResourceWithRawResponse(self.providers)

    @cached_property
    def openai(self) -> AsyncOpenAIResourceWithRawResponse:
        return AsyncOpenAIResourceWithRawResponse(self.providers)