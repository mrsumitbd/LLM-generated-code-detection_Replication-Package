from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .providers import AsyncProvidersResource
    from .anthropic import AsyncAnthropicResourceWithRawResponse
    from .openai import AsyncOpenAIResourceWithRawResponse


class AsyncProvidersResourceWithRawResponse:
    """
    A wrapper around :class:`AsyncProvidersResource` that exposes the same
    provider resources but with raw-response capabilities.
    """

    def __init__(self, providers: "AsyncProvidersResource") -> None:
        self._providers = providers

    @cached_property
    def anthropic(self) -> "AsyncAnthropicResourceWithRawResponse":
        """
        Return the Anthropic provider wrapped with raw-response support.
        """
        return AsyncAnthropicResourceWithRawResponse(self._providers.anthropic)

    @cached_property
    def openai(self) -> "AsyncOpenAIResourceWithRawResponse":
        """
        Return the OpenAI provider wrapped with raw-response support.
        """
        return AsyncOpenAIResourceWithRawResponse(self._providers.openai)