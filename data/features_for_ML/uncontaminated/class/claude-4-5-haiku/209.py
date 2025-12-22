from typing import Callable, Dict, Any, List, Set
from collections import defaultdict
import threading
from datetime import datetime


class RealTimeContextUpdater:
    """Manage real-time context updates during incidents."""

    def __init__(self, server_instance=None):
        self.server_instance = server_instance
        self._context_callbacks: Dict[str, Set[Callable]] = defaultdict(set)
        self._global_callbacks: Set[Callable] = set()
        self._lock = threading.RLock()
        self._update_count = 0
        self._subscription_count = 0
        self._start_time = datetime.now()

    def subscribe_to_updates(self, context_id: str, callback: Callable) -> None:
        """Subscribe a callback to updates for a specific context."""
        with self._lock:
            if callback not in self._context_callbacks[context_id]:
                self._context_callbacks[context_id].add(callback)
                self._subscription_count += 1

    def unsubscribe_from_updates(self, context_id: str, callback: Callable) -> None:
        """Unsubscribe a callback from updates for a specific context."""
        with self._lock:
            if context_id in self._context_callbacks:
                self._context_callbacks[context_id].discard(callback)
                self._subscription_count = max(0, self._subscription_count - 1)
                if not self._context_callbacks[context_id]:
                    del self._context_callbacks[context_id]

    def subscribe_to_all_updates(self, callback: Callable) -> None:
        """Subscribe a callback to all context updates."""
        with self._lock:
            if callback not in self._global_callbacks:
                self._global_callbacks.add(callback)
                self._subscription_count += 1

    def unsubscribe_from_all_updates(self, callback: Callable) -> None:
        """Unsubscribe a callback from all context updates."""
        with self._lock:
            if callback in self._global_callbacks:
                self._global_callbacks.discard(callback)
                self._subscription_count = max(0, self._subscription_count - 1)

    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics for the updater."""
        with self._lock:
            uptime = (datetime.now() - self._start_time).total_seconds()
            total_contexts = len(self._context_callbacks)
            total_context_subscriptions = sum(
                len(callbacks) for callbacks in self._context_callbacks.values()
            )
            global_subscriptions = len(self._global_callbacks)
            
            return {
                "uptime_seconds": uptime,
                "total_contexts_monitored": total_contexts,
                "total_context_subscriptions": total_context_subscriptions,
                "global_subscriptions": global_subscriptions,
                "total_subscriptions": self._subscription_count,
                "total_updates_processed": self._update_count,
                "active_callbacks": total_context_subscriptions + global_subscriptions,
            }