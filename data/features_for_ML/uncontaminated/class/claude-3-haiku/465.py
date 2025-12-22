from cached_property import cached_property
from .async_providers_resource import AsyncProvidersResource
from .async_anthropic_resource_with_raw_response import AsyncAnthropicResourceWithRawResponse
from .async_openai_resource_with_raw_response import AsyncOpenAIResourceWithRawResponse

class AsyncProvidersResourceWithRawResponse:

    def __init__(self, providers: AsyncProvidersResource) -> None:
        self._providers = providers

    @cached_property
    def anthropic(self) -> AsyncAnthropicResourceWithRawResponse:
        return AsyncAnthropicResourceWithRawResponse(self._providers.anthropic)

    @cached_property
    def openai(self) -> AsyncOpenAIResourceWithRawResponse:
        return AsyncOpenAIResourceWithRawResponse(self._providers.openai)