import inspect
import functools
from typing import Any, Awaitable, Callable


class AsyncTrendingSearchResourceWithStreamingResponse:
    """
    A wrapper around :class:`AsyncTrendingSearchResource` that automatically
    enables streaming for all async methods that accept a ``stream`` keyword
    argument.
    """

    def __init__(self, trending_search: Any) -> None:
        """
        Parameters
        ----------
        trending_search : AsyncTrendingSearchResource
            The underlying async resource to wrap.
        """
        self._trending_search = trending_search

    def __getattr__(self, name: str) -> Any:
        """
        Forward attribute access to the underlying resource. If the attribute
        is a coroutine function that accepts a ``stream`` parameter, the
        wrapper will automatically set ``stream=True`` unless the caller
        explicitly overrides it.
        """
        attr = getattr(self._trending_search, name)

        if not callable(attr):
            return attr

        @functools.wraps(attr)
        async def wrapper(*args: Any, **kwargs: Any) -> Awaitable[Any]:
            # Inspect the signature to see if ``stream`` is a valid keyword.
            try:
                sig = inspect.signature(attr)
                if "stream" in sig.parameters:
                    kwargs.setdefault("stream", True)
            except (ValueError, TypeError):
                # If the signature cannot be inspected, just forward the call.
                pass

            return await attr(*args, **kwargs)

        return wrapper