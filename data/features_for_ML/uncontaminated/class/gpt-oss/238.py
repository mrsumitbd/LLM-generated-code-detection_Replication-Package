from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, Tuple, Union

# The actual AsyncSnapshotsResource type is expected to be defined elsewhere.
# We use a forward reference for type checking purposes.
class AsyncSnapshotsResourceWithRawResponse:
    """
    A wrapper around :class:`AsyncSnapshotsResource` that returns raw HTTP responses.
    """

    def __init__(self, snapshots: "AsyncSnapshotsResource") -> None:
        """
        Initialize the wrapper.

        Parameters
        ----------
        snapshots:
            The underlying async snapshots resource.
        """
        self._snapshots = snapshots

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the underlying snapshots resource.

        If the attribute is a coroutine function, wrap it so that the
        ``raw_response`` keyword argument is automatically set to ``True``.
        """
        attr = getattr(self._snapshots, name)

        if callable(attr):
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                # Ensure the raw_response flag is set.
                kwargs.setdefault("raw_response", True)
                return await attr(*args, **kwargs)

            # Preserve the original function's metadata for introspection.
            wrapper.__name__ = attr.__name__
            wrapper.__doc__ = attr.__doc__
            wrapper.__qualname__ = attr.__qualname__
            return wrapper

        return attr

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} wrapping {self._snapshots!r}>"