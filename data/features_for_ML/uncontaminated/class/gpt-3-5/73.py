from enum import Enum
from typing import Callable, Any

class Events:

    class Types(Enum):
        EVENT_1 = 1
        EVENT_2 = 2
        EVENT_3 = 3

    def __init__(self):
        self.subscribers = {}

    def reset(self):
        self.subscribers = {}

    def subscribe(self, event_type: Types, callback: Callable, ephemeral: bool = False) -> None:
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append((callback, ephemeral))

    def unsubscribe(self, event_type: Types, callback: Callable) -> None:
        if event_type in self.subscribers:
            self.subscribers[event_type] = [(cb, ephem) for cb, ephem in self.subscribers[event_type] if cb != callback]

    def emit(self, event_type: Types, *args: Any, **kwargs: Any) -> None:
        if event_type in self.subscribers:
            for callback, ephemeral in self.subscribers[event_type]:
                callback(*args, **kwargs)
                if ephemeral:
                    self.unsubscribe(event_type, callback)