from __future__ import annotations

from typing import Any, Awaitable, Callable, Coroutine, TypeVar, overload

T = TypeVar("T")


class AsyncInfoResourceWithRawResponse:
    """
    A thin wrapper around an :class:`AsyncInfoResource` that forwards all
    attribute access and method calls to the underlying resource.  The wrapper
    is intended to expose the raw HTTP responses from the underlying
    asynchronous resource.  It does not alter the behaviour of the wrapped
    resource; it simply delegates calls.
    """

    def __init__(self, info: Any) -> None:
        """
        Create a new wrapper around the given async info resource.

        Parameters
        ----------
        info : Any
            The async info resource to wrap.  It is expected to provide the
            same public API as the original resource.
        """
        self._info = info

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the wrapped resource.

        If the attribute is a coroutine function, a new coroutine is returned
        that awaits the original coroutine.  For all other attributes the
        original value is returned unchanged.
        """
        attr = getattr(self._info, name)

        if callable(attr):
            # Preserve the coroutine nature of async methods.
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                return await attr(*args, **kwargs)

            # Preserve the original function's metadata.
            wrapper.__name__ = attr.__name__
            wrapper.__doc__ = attr.__doc__
            wrapper.__qualname__ = attr.__qualname__
            return wrapper

        return attr