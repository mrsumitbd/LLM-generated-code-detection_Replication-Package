from __future__ import annotations

from typing import Any, Callable, Iterable, Iterator, Mapping, MutableMapping, Sequence, Tuple, Union


class ActionsResourceWithStreamingResponse:
    """
    A wrapper around an :class:`ActionsResource` that exposes the same API but returns
    streaming responses. The wrapper simply forwards all public callable attributes
    to the underlying resource. If a method returns an iterable, it will be yielded
    as a stream.
    """

    def __init__(self, actions: Any) -> None:
        """
        Initialize the streaming response wrapper.

        Parameters
        ----------
        actions : Any
            The underlying :class:`ActionsResource` instance to wrap.
        """
        self._actions = actions

        # Dynamically expose all public callables from the underlying resource.
        for attr_name in dir(actions):
            if attr_name.startswith("_"):
                continue
            attr = getattr(actions, attr_name)
            if callable(attr):
                # Create a wrapper that forwards the call to the underlying method.
                def _make_wrapper(method: Callable[..., Any]) -> Callable[..., Any]:
                    def wrapper(*args: Any, **kwargs: Any) -> Any:
                        return method(*args, **kwargs)

                    # Preserve the original method's name and docstring.
                    wrapper.__name__ = method.__name__
                    wrapper.__doc__ = method.__doc__
                    return wrapper

                setattr(self, attr_name, _make_wrapper(attr))

    def __getattr__(self, name: str) -> Any:
        """
        Fallback attribute access to the underlying actions resource.
        """
        return getattr(self._actions, name)