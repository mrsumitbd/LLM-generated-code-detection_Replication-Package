from typing import Callable, Dict, Any

class RealTimeContextUpdater:
    """Manage real-time context updates during incidents."""

    def __init__(self, server_instance=None):
        self.server_instance = server_instance
        self.context_callbacks = {}
        self.all_updates_callbacks = []

    def subscribe_to_updates(self, context_id: str, callback: Callable) -> None:
        if context_id not in self.context_callbacks:
            self.context_callbacks[context_id] = []
        self.context_callbacks[context_id].append(callback)

    def unsubscribe_from_updates(self, context_id: str, callback: Callable) -> None:
        if context_id in self.context_callbacks:
            self.context_callbacks[context_id].remove(callback)
            if not self.context_callbacks[context_id]:
                del self.context_callbacks[context_id]

    def subscribe_to_all_updates(self, callback: Callable) -> None:
        self.all_updates_callbacks.append(callback)

    def unsubscribe_from_all_updates(self, callback: Callable) -> None:
        self.all_updates_callbacks.remove(callback)

    def get_monitoring_stats(self) -> Dict[str, Any]:
        return {
            "num_context_subscriptions": sum(len(callbacks) for callbacks in self.context_callbacks.values()),
            "num_all_updates_subscriptions": len(self.all_updates_callbacks),
        }