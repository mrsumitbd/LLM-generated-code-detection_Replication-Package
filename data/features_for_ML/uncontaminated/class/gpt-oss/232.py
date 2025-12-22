import asyncio
import functools
from typing import Any, Awaitable


class AsyncAutoscaleResourceWithStreamingResponse:
    """
    A wrapper around an AsyncAutoscaleResource that forwards all attribute
    access to the underlying resource. Coroutine methods are wrapped to
    preserve their async nature.
    """

    def __init__(self, autoscale: Any) -> None:
        """
        Initialize the wrapper with the given AsyncAutoscaleResource instance.

        Parameters
        ----------
        autoscale : Any
            The underlying async autoscale resource to wrap.
        """
        self._autoscale = autoscale

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the underlying autoscale resource.

        If the attribute is an async coroutine function, it is wrapped in an
        async function that simply awaits the original coroutine. This
        ensures that the wrapper behaves transparently for async methods.
        """
        attr = getattr(self._autoscale, name)

        if asyncio.iscoroutinefunction(attr):
            @functools.wraps(attr)
            async def wrapper(*args: Any, **kwargs: Any) -> Awaitable[Any]:
                return await attr(*args, **kwargs)

            return wrapper

        return attr