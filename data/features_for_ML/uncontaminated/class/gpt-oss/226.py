from __future__ import annotations

from typing import Callable, List, Any, Iterable, Union

# The following imports are placeholders. In a real project these would be
# imported from the actual modules that define Config, Trainer, and Callback.
# They are kept here only to satisfy type checkers and to make the code
# self‑contained for demonstration purposes.
try:
    from some_module import Config, Trainer, Callback  # type: ignore
except Exception:  # pragma: no cover
    # Minimal stubs for type checking / demonstration
    class Config:
        callbacks: Iterable[Any] = []

    class Trainer:
        pass

    class Callback:
        pass


class CallBackGroup:
    """A class for hosting a collection of callback objects.

    It is used to execute callback functions of multiple callback objects with the same method name.
    When callbackgroup.func(args) is executed, internally it loops through the objects in self._callbacks
    and runs
    self._callbacks[0].func(args), self._callbacks[1].func(args), etc. The method name and arguments
    should match.

    Attributes:
        _callbacks (list[Callback]): List of callback objects.
    """

    def __init__(self, config: Config, trainer: Trainer) -> None:
        """
        Create a CallBackGroup from a configuration and a trainer.

        Parameters
        ----------
        config : Config
            Configuration object that contains a ``callbacks`` attribute.
            The attribute may be an iterable of callback instances or
            callback classes.  If a class is provided, it will be
            instantiated with the trainer as its sole argument.
        trainer : Trainer
            Trainer instance that will be passed to callback constructors
            when needed.
        """
        callbacks: List[Callback] = []

        # The config may expose callbacks in several ways.  We try to be
        # tolerant: if it has a ``callbacks`` attribute, we use it; otherwise
        # we fall back to an empty list.
        callback_sources = getattr(config, "callbacks", [])

        for cb in callback_sources:
            # If the callback is already an instance, keep it.
            if isinstance(cb, Callback):
                callbacks.append(cb)
            # If the callback is a class (or any callable that can be
            # instantiated with a trainer), instantiate it.
            elif callable(cb):
                try:
                    instance = cb(trainer)  # type: ignore
                    if isinstance(instance, Callback):
                        callbacks.append(instance)
                    else:
                        # If the constructor did not return a Callback,
                        # we ignore it to avoid runtime errors.
                        pass
                except Exception:
                    # If instantiation fails, skip this callback.
                    pass
            else:
                # Unsupported type; ignore.
                pass

        self._callbacks: List[Callback] = callbacks

    def __getattr__(self, method_name: str) -> Callable:
        """
        Dynamically create a dispatcher for a callback method.

        When an attribute that does not exist on the group itself is
        accessed, this method returns a callable that, when invoked,
        forwards the call to the same method on each callback in the
        group (if that method exists).

        Parameters
        ----------
        method_name : str
            Name of the method to dispatch.

        Returns
        -------
        Callable
            A function that forwards its arguments to the corresponding
            method on each callback.
        """
        def dispatcher(*args: Any, **kwargs: Any) -> None:
            for cb in self._callbacks:
                method = getattr(cb, method_name, None)
                if callable(method):
                    method(*args, **kwargs)

        return dispatcher