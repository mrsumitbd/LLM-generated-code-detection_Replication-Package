from typing import Any

class SSEEventManager:
    """
    Centralized SSE connection management and event broadcasting.

    Manages multiple SSE connections and broadcasts events to all connected clients.
    Uses bounded queues to prevent memory issues with slow clients.
    """

    def __init__(self, max_queue_size: int = 100) -> None:
        self.max_queue_size = max_queue_size

    def _format_sse_event(self, event: dict[str, Any]) -> str:
        formatted_event = f"data: {json.dumps(event, default=self._json_serializer)}\n\n"
        return formatted_event

    def _json_serializer(self, obj: Any) -> Any:
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")