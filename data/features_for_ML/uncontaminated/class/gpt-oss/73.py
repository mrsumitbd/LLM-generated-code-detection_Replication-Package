from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Tuple


class Events:
    """
    A simple event dispatcher that allows subscribing callbacks to named event types,
    unsubscribing them, emitting events, and resetting all subscriptions.
    """

    class Types(Enum):
        """
        Placeholder enum for event types. Users can extend this enum or use any hashable
        value as an event type; the enum is only used for type hinting.
        """
        # Example placeholder member; users may define their own members.
        ANY = auto()

    @dataclass
    class _Subscriber:
        callback: Callable
        is_ephemeral: bool

    def __init__(self) -> None:
        # Mapping from event_type to list of _Subscriber objects
        self._subscribers: Dict[Any, List[Events._Subscriber]] = defaultdict(list)

    def reset(self) -> None:
        """Remove all event subscriptions."""
        self._subscribers.clear()

    def subscribe(
        self,
        event_type: Events.Types,
        callback: Callable,
        *,
        ephemeral: bool = False,
    ) -> None:
        """
        Register a callback to be invoked when the specified event_type is emitted.

        Parameters
        ----------
        event_type : Events.Types
            The event type to subscribe to.
        callback : Callable
            The function to call when the event is emitted.
        ephemeral : bool, optional
            If True, the callback will be removed after the first invocation.
        """
        if not callable(callback):
            raise TypeError("callback must be callable")
        self._subscribers[event_type].append(
            Events._Subscriber(callback=callback, is_ephemeral=ephemeral)
        )

    def unsubscribe(self, event_type: Events.Types, callback: Callable) -> None:
        """
        Remove a previously registered callback for the given event_type.

        Parameters
        ----------
        event_type : Events.Types
            The event type to unsubscribe from.
        callback : Callable
            The callback function to remove.
        """
        subs = self._subscribers.get(event_type)
        if not subs:
            return
        # Remove all matching callbacks
        self._subscribers[event_type] = [
            sub for sub in subs if sub.callback is not callback
        ]
        # Clean up empty list to avoid memory leak
        if not self._subscribers[event_type]:
            del self._subscribers[event_type]

    def emit(self, event_type: Events.Types, *args: Any, **kwargs: Any) -> None:
        """
        Emit an event, invoking all subscribed callbacks with the provided arguments.

        Parameters
        ----------
        event_type : Events.Types
            The event type to emit.
        *args, **kwargs
            Arguments to pass to the callbacks.
        """
        subs = self._subscribers.get(event_type)
        if not subs:
            return

        # Make a copy to allow modification during iteration
        for sub in list(subs):
            try:
                sub.callback(*args, **kwargs)
            except Exception:
                # Swallow exceptions to ensure all callbacks are attempted
                # Users can attach logging if needed
                pass
            if sub.is_ephemeral:
                self.unsubscribe(event_type, sub.callback)