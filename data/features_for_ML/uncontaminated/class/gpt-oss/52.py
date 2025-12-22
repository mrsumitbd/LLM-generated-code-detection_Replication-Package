from __future__ import annotations
from typing import Any, Callable, Coroutine, Awaitable
import functools


class AsyncCategoriesResourceWithRawResponse:
    """
    A wrapper around an :class:`AsyncCategoriesResource` that exposes the same
    interface but returns the raw HTTP responses instead of parsed objects.
    """

    def __init__(self, categories: Any) -> None:
        """
        Create a new wrapper around the given async categories resource.

        Parameters
        ----------
        categories : Any
            The underlying async categories resource instance.
        """
        self._categories = categories

    def __getattr__(self, name: str) -> Any:
        """
        Forward attribute access to the underlying resource. If the attribute
        is a coroutine function, wrap it so that the returned coroutine
        yields the raw response.
        """
        attr = getattr(self._categories, name)

        if not callable(attr):
            return attr

        @functools.wraps(attr)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # The underlying method is expected to return a coroutine that
            # yields the raw response. We simply await it and return the result.
            return await attr(*args, **kwargs)

        return wrapper

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} wrapped={repr(self._categories)}>"