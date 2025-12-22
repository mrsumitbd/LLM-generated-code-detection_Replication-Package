from typing import Callable, Dict, Any, Set
import threading
import time


class RealTimeContextUpdater:
    """Manage real-time context updates during incidents."""

    def __init__(self, server_instance=None):
        self._server = server_instance
        self._context_callbacks: Dict[str, Set[Callable]] = {}
        self._global_callbacks: Set[Callable] = set()
        self._lock = threading.RLock()
        self._last_update_ts = 0.0
        self._update_count = 0

    def subscribe_to_updates(self, context_id: str, callback: Callable) -> None:
        with self._lock:
            self._context_callbacks.setdefault(context_id, set()).add(callback)

    def unsubscribe_from_updates(self, context_id: str, callback: Callable) -> None:
        with self._lock:
            callbacks = self._context_callbacks.get(context_id)
            if callbacks and callback in callbacks:
                callbacks.remove(callback)
                if not callbacks:
                    del self._context_callbacks[context_id]

    def subscribe_to_all_updates(self, callback: Callable) -> None:
        with self._lock:
            self._global_callbacks.add(callback)

    def unsubscribe_from_all_updates(self, callback: Callable) -> None:
        with self._lock:
            self._global_callbacks.discard(callback)

    def _notify(self, context_id: str, data: Any) -> None:
        with self._lock:
            callbacks = self._context_callbacks.get(context_id, set()).copy()
            global_callbacks = self._global_callbacks.copy()
        for cb in callbacks:
            try:
                cb(context_id, data)
            except Exception:
                pass
        for cb in global_callbacks:
            try:
                cb(context_id, data)
            except Exception:
                pass
        with self._lock:
            self._last_update_ts = time.time()
            self._update_count += 1

    def get_monitoring_stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "contexts_subscribed": len(self._context_callbacks),
                "total_callbacks": sum(len(cbs) for cbs in self._context_callbacks.values()) + len(self._global_callbacks),
                "global_callbacks": len(self._global_callbacks),
                "last_update_ts": self._last_update_ts,
                "update_count": self._update_count,
            }