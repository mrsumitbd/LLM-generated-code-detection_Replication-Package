import inspect
from typing import Any, AsyncIterator, Callable, Coroutine, Union


class AsyncOhlcvResourceWithStreamingResponse:
    """
    A wrapper around an :class:`AsyncOhlcvResource` that exposes all of its
    asynchronous methods as streaming responses.  If the underlying method
    returns an async iterator, that iterator is returned unchanged.  If the
    method returns a normal awaitable, the result is wrapped in an async
    generator that yields the single value.
    """

    def __init__(self, ohlcv: Any) -> None:
        """
        Create a new streaming wrapper.

        Parameters
        ----------
        ohlcv:
            The underlying :class:`AsyncOhlcvResource` instance.
        """
        self._ohlcv = ohlcv

    def __getattr__(self, name: str) -> Any:
        """
        Forward attribute access to the underlying resource.  If the
        attribute is an async function, return a wrapper that yields a
        streaming response.
        """
        attr = getattr(self._ohlcv, name)

        # If the attribute is a coroutine function, wrap it.
        if inspect.iscoroutinefunction(attr):
            async def wrapper(*args: Any, **kwargs: Any) -> AsyncIterator[Any]:
                # Await the original coroutine.
                result = await attr(*args, **kwargs)

                # If the result itself is an async iterator, return it.
                if hasattr(result, "__aiter__"):
                    return result

                # Otherwise, wrap the single result in an async generator.
                async def generator() -> AsyncIterator[Any]:
                    yield result

                return generator()

            return wrapper

        # For non-async attributes, just forward them unchanged.
        return attr