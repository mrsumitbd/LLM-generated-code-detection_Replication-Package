from __future__ import annotations
from typing import Any, Callable, Awaitable, TypeVar, overload

T = TypeVar("T")


class AsyncJobResourceWithRawResponse:
    """
    A wrapper around an :class:`AsyncJobResource` that forwards all attribute
    access to the underlying resource.  Async methods are wrapped so that
    they can be awaited directly.
    """

    def __init__(self, job: Any) -> None:
        """
        Create a new wrapper around the given async job resource.

        Parameters
        ----------
        job:
            The underlying async job resource to wrap.
        """
        self._job = job

    def __getattr__(self, name: str) -> Any:
        """
        Forward attribute access to the underlying job resource.

        If the attribute is a coroutine function, it is wrapped so that it can
        be awaited directly.  All other attributes are returned unchanged.
        """
        attr = getattr(self._job, name)

        if callable(attr):
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                return await attr(*args, **kwargs)

            # Preserve the original function's metadata
            wrapper.__name__ = attr.__name__
            wrapper.__doc__ = attr.__doc__
            wrapper.__qualname__ = attr.__qualname__
            return wrapper

        return attr