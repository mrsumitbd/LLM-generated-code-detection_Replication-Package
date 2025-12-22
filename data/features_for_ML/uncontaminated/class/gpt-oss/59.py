from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .resources import OpenAIResource, KeysResourceWithStreamingResponse

class OpenAIResourceWithStreamingResponse:
    """
    A wrapper around :class:`OpenAIResource` that exposes streaming-enabled
    sub‑resources.  Each sub‑resource is lazily instantiated and cached.
    """

    def __init__(self, openai: "OpenAIResource") -> None:
        """
        Parameters
        ----------
        openai:
            The underlying :class:`OpenAIResource` instance.
        """
        self._openai = openai

    @cached_property
    def keys(self) -> "KeysResourceWithStreamingResponse":
        """
        Return a streaming‑enabled wrapper around the ``keys`` sub‑resource.
        """
        return KeysResourceWithStreamingResponse(self._openai.keys)