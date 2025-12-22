from __future__ import annotations
from typing import Callable, Optional, Dict, Any
import datetime


class FlowEnvironment:
    """
    A class to represent the state of a workflow.
    """

    def __init__(self, name: str, flog: Optional[Callable[..., None]] = None, fstate: Optional[Dict[str, Any]] = None):
        """
        Initialise a new FlowEnvironment.

        Parameters
        ----------
        name : str
            The name of the environment.
        flog : Callable[..., None], optional
            A logging function that accepts arbitrary arguments.
        fstate : dict, optional
            A dictionary representing the initial state.
        """
        self.name = name
        self.flog = flog or (lambda *_, **__: None)
        self.fstate: Dict[str, Any] = fstate or {}
        self._alive: bool = True
        self._last_refresh: Optional[datetime.datetime] = None
        self.refresh()

    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------
    def refresh(self, t: Optional[datetime.datetime] = None) -> None:
        """
        Update the last refresh timestamp.

        Parameters
        ----------
        t : datetime.datetime, optional
            The timestamp to use; if None, the current time is used.
        """
        self._last_refresh = t or datetime.datetime.now()
        self.flog(f"[{self.name}] refreshed at {self._last_refresh}")

    def kill(self) -> Dict[str, Any]:
        """
        Terminate the environment and return its state.

        Returns
        -------
        dict
            A copy of the current state before it was cleared.
        """
        self._alive = False
        state = self.fstate.copy()
        self.fstate.clear()
        self.flog(f"[{self.name}] killed")
        return state

    def still_alive(self) -> bool:
        """
        Check whether the environment is still alive.

        Returns
        -------
        bool
            True if alive, False otherwise.
        """
        return self._alive

    def dump(self) -> None:
        """
        Dump the current state to the log.
        """
        self.flog(f"[{self.name}] state: {self.fstate}")

    def get(self) -> Dict[str, Any]:
        """
        Return the current state dictionary.

        Returns
        -------
        dict
            The current state.
        """
        return self.fstate

    def rejuvenate(self) -> None:
        """
        Reset the environment to an alive state.
        """
        self._alive = True
        self.flog(f"[{self.name}] rejuvenated")

    # ------------------------------------------------------------------
    # Execution helpers
    # ------------------------------------------------------------------
    def run(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        """
        Execute a function within the environment.

        Parameters
        ----------
        func : Callable
            The function to execute.
        *args, **kwargs
            Arguments to pass to the function.

        Returns
        -------
        Any
            The result of the function call.
        """
        self.flog(f"[{self.name}] running {func.__name__}")
        return func(*args, **kwargs)

    def decorate(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator that logs before and after calling the function.

        Parameters
        ----------
        func : Callable
            The function to decorate.

        Returns
        -------
        Callable
            The wrapped function.
        """
        def wrapper(*args, **kwargs):
            self.flog(f"[{self.name}] entering {func.__name__}")
            result = func(*args, **kwargs)
            self.flog(f"[{self.name}] exiting {func.__name__}")
            return result
        return wrapper

    @staticmethod
    def static_decorate(fstate: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        A static decorator that injects a state key into the function's kwargs.

        Parameters
        ----------
        fstate : str, optional
            The key to inject into kwargs.

        Returns
        -------
        Callable
            A decorator that injects the key.
        """
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            def wrapper(*args, **kwargs):
                if fstate is not None:
                    kwargs[fstate] = kwargs.get(fstate, None)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Allow the environment instance to be used as a decorator.
        """
        return self.decorate(func)

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------
    def __enter__(self) -> "FlowEnvironment":
        self.flog(f"[{self.name}] entering context")
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if exc_type:
            self.flog(f"[{self.name}] exception: {exc_value}")
        self.flog(f"[{self.name}] exiting context")
        # Returning False propagates exceptions
        return False

    # ------------------------------------------------------------------
    # String representations
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return f"FlowEnvironment(name={self.name})"

    def __repr__(self) -> str:
        return f"<FlowEnvironment {self.name} alive={self._alive}>"