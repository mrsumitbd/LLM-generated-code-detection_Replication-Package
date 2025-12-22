from typing import Any, Callable, Dict, Iterator, Optional
from functools import cached_property

from openai.api_resources.abstract.api_resource import APIResource
from openai.api_resources.abstract.streaming_api_resource import StreamingAPIResource
from openai.api_resources.key import KeysResourceWithStreamingResponse

class OpenAIResourceWithStreamingResponse(StreamingAPIResource):
    def __init__(self, openai: OpenAIResource) -> None:
        self._openai = openai

    @cached_property
    def keys(self) -> KeysResourceWithStreamingResponse:
        return KeysResourceWithStreamingResponse(self._openai)

    def create(self, **params: Any) -> Iterator[Dict[str, Any]]:
        return self._openai.create_stream(**params)

    def retrieve(self, id: str, **params: Any) -> Iterator[Dict[str, Any]]:
        return self._openai.retrieve_stream(id, **params)

    def update(self, id: str, **params: Any) -> Iterator[Dict[str, Any]]:
        return self._openai.update_stream(id, **params)

    def delete(self, id: str, **params: Any) -> Iterator[Dict[str, Any]]:
        return self._openai.delete_stream(id, **params)