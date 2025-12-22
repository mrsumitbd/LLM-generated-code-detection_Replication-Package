from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .openai_resource import OpenAIResource
    from .keys_resource_with_raw_response import KeysResourceWithRawResponse

class OpenAIResourceWithRawResponse:
    """
    A wrapper around :class:`OpenAIResource` that exposes the same resources
    but with raw response support.
    """

    def __init__(self, openai: "OpenAIResource") -> None:
        """
        Initialize the wrapper.

        Parameters
        ----------
        openai : OpenAIResource
            The underlying OpenAI resource instance.
        """
        self._openai = openai

    @cached_property
    def keys(self) -> "KeysResourceWithRawResponse":
        """
        Return the keys resource wrapped with raw response support.

        Returns
        -------
        KeysResourceWithRawResponse
            The wrapped keys resource.
        """
        from .keys_resource_with_raw_response import KeysResourceWithRawResponse

        return KeysResourceWithRawResponse(self._openai.keys)