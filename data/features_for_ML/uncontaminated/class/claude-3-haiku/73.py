from typing import Callable, Any, Dict, List

class Events:
    class Types:
        pass

    def __init__(self):
        self._subscriptions: Dict[Events.Types, List[Callable]] = {}

    def reset(self):
        self._subscriptions.clear()

    def subscribe(self, event_type: Events.Types, callback: Callable, ephemeral: bool = False) -> None:
        if event_type not in self._subscriptions:
            self._subscriptions[event_type] = []
        self._subscriptions[event_type].append(callback)

    def unsubscribe(self, event_type: Events.Types, callback: Callable) -> None:
        if event_type in self._subscriptions:
            self._subscriptions[event_type].remove(callback)

    def emit(self, event_type: Events.Types, *args: Any, **kwargs: Any) -> None:
        if event_type in self._subscriptions:
            for callback in self._subscriptions[event_type]:
                callback(*args, **kwargs)