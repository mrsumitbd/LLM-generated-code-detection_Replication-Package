import asyncio
from functools import wraps
from typing import Any, Callable, Coroutine


class AsyncFunctionsResourceWithRawResponse:
    """
    A wrapper around an :class:`AsyncFunctionsResource` that forwards all
    attribute access to the underlying resource.  Async methods are wrapped
    so that they can be awaited directly from the wrapper.
    """

    def __init__(self, functions: Any) -> None:
        """
        Create a new wrapper around the given async functions resource.

        Parameters
        ----------
        functions : Any
            The async functions resource to wrap.  It is expected to expose
            async methods that perform HTTP requests.
        """
        self._functions = functions

    def __getattr__(self, name: str) -> Any:
        """
        Forward attribute access to the underlying resource.  If the
        attribute is an async function, return a coroutine that awaits
        the underlying function.
        """
        attr = getattr(self._functions, name)

        if asyncio.iscoroutinefunction(attr):
            @wraps(attr)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                return await attr(*args, **kwargs)

            return wrapper

        return attr