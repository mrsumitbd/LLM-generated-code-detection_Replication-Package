from __future__ import annotations

from typing import Any, Callable

# The streaming wrapper is used to convert normal responses into streaming ones.
# It is part of the OpenAI SDK's internal utilities.
try:
    from openai._streaming import to_streaming_response_wrapper
except Exception:  # pragma: no cover
    # Fallback stub in case the import path changes or the module is not available.
    def to_streaming_response_wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        """Fallback wrapper that simply returns the original function."""
        return func


class TopHoldersResourceWithStreamingResponse:
    """
    A wrapper around :class:`TopHoldersResource` that exposes all of its
    callable attributes as streaming responses.
    """

    def __init__(self, top_holders: Any) -> None:
        """
        Initialize the streaming wrapper.

        Parameters
        ----------
        top_holders : TopHoldersResource
            The underlying resource instance to wrap.
        """
        self._top_holders = top_holders

        # Dynamically wrap all public callables of the underlying resource.
        for attr_name in dir(top_holders):
            if attr_name.startswith("_"):
                continue
            attr = getattr(top_holders, attr_name)
            if callable(attr):
                setattr(self, attr_name, to_streaming_response_wrapper(attr))