import json
from typing import Any
from collections import deque
from threading import Lock

class SSEEventManager:
    """
    Centralized SSE connection management and event broadcasting.

    Manages multiple SSE connections and broadcasts events to all connected clients.
    Uses bounded queues to prevent memory issues with slow clients.
    """

    def __init__(self, max_queue_size: int = 100) -> None:
        self.connections = {}
        self.lock = Lock()
        self.max_queue_size = max_queue_size

    def _format_sse_event(self, event: dict[str, Any]) -> str:
        lines = []
        for key, value in event.items():
            lines.append(f"{key}: {value}")
        lines.append("data: {}")
        return "\n".join(lines) + "\n\n"

    def _json_serializer(self, obj: Any) -> Any:
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return json.dumps(obj)

    def register_connection(self, connection_id: str) -> None:
        with self.lock:
            self.connections[connection_id] = deque(maxlen=self.max_queue_size)

    def unregister_connection(self, connection_id: str) -> None:
        with self.lock:
            del self.connections[connection_id]

    def broadcast_event(self, event: dict[str, Any]) -> None:
        sse_event = self._format_sse_event(event)
        with self.lock:
            for queue in self.connections.values():
                queue.append(sse_event)

    def get_events(self, connection_id: str) -> str:
        with self.lock:
            queue = self.connections[connection_id]
            events = "".join(queue)
            queue.clear()
            return events