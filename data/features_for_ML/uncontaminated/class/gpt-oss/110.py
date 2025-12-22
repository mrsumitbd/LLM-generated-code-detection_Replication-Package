from __future__ import annotations
from typing import Any, Callable, Awaitable, Union

class AsyncOhlcvResourceWithRawResponse:
    """
    A wrapper around an AsyncOhlcvResource that exposes the raw HTTP response
    when available. If the underlying method returns an object with a `raw`
    attribute, that attribute is returned. If the method returns a tuple,
    the second element is returned. Otherwise the original result is returned.
    """

    def __init__(self, ohlcv: Any) -> None:
        """
        Initialize the wrapper with an AsyncOhlcvResource instance.

        Parameters
        ----------
        ohlcv : Any
            The underlying AsyncOhlcvResource instance to wrap.
        """
        self._ohlcv = ohlcv

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the underlying AsyncOhlcvResource.

        If the attribute is a coroutine function, wrap it so that the raw
        response is returned when available.

        Parameters
        ----------
        name : str
            The attribute name to retrieve.

        Returns
        -------
        Any
            The attribute from the underlying resource, possibly wrapped.
        """
        attr = getattr(self._ohlcv, name)

        if callable(attr):
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = await attr(*args, **kwargs)
                # Prefer a `raw` attribute if present
                if hasattr(result, "raw"):
                    return result.raw
                # If the result is a tuple, return the second element
                if isinstance(result, tuple) and len(result) > 1:
                    return result[1]
                return result

            return wrapper

        return attr