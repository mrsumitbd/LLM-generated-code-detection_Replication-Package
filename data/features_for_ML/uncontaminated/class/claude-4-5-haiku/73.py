from typing import Callable, Any, Dict, List
from enum import Enum

class Events:
    
    class Types(Enum):
        pass
    
    def __init__(self):
        self._subscribers: Dict[Events.Types, List[tuple]] = {}
    
    def reset(self):
        self._subscribers.clear()
    
    def subscribe(self, event_type: Events.Types, callback: Callable, ephemeral: bool = False) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append((callback, ephemeral))
    
    def unsubscribe(self, event_type: Events.Types, callback: Callable) -> None:
        if event_type in self._subscribers:
            self._subscribers[event_type] = [
                (cb, eph) for cb, eph in self._subscribers[event_type] if cb != callback
            ]
            if not self._subscribers[event_type]:
                del self._subscribers[event_type]
    
    def emit(self, event_type: Events.Types, *args: Any, **kwargs: Any) -> None:
        if event_type not in self._subscribers:
            return
        
        ephemeral_callbacks = []
        for callback, is_ephemeral in self._subscribers[event_type]:
            callback(*args, **kwargs)
            if is_ephemeral:
                ephemeral_callbacks.append(callback)
        
        for callback in ephemeral_callbacks:
            self.unsubscribe(event_type, callback)