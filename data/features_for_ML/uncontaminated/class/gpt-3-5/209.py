from typing import Callable, Dict, Any

class RealTimeContextUpdater:
    """Manage real-time context updates during incidents."""

    def __init__(self, server_instance=None):
        self.server_instance = server_instance
        self.context_subscriptions = {}

    def subscribe_to_updates(self, context_id: str, callback: Callable) -> None:
        if context_id not in self.context_subscriptions:
            self.context_subscriptions[context_id] = []
        self.context_subscriptions[context_id].append(callback)

    def unsubscribe_from_updates(self, context_id: str, callback: Callable) -> None:
        if context_id in self.context_subscriptions:
            if callback in self.context_subscriptions[context_id]:
                self.context_subscriptions[context_id].remove(callback)

    def subscribe_to_all_updates(self, callback: Callable) -> None:
        for context_id in self.context_subscriptions:
            self.context_subscriptions[context_id].append(callback)

    def unsubscribe_from_all_updates(self, callback: Callable) -> None:
        for context_id in self.context_subscriptions:
            if callback in self.context_subscriptions[context_id]:
                self.context_subscriptions[context_id].remove(callback)

    def get_monitoring_stats(self) -> Dict[str, Any]:
        stats = {}
        for context_id, callbacks in self.context_subscriptions.items():
            stats[context_id] = len(callbacks)
        return stats