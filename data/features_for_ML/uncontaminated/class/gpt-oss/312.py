import asyncio
import json
from typing import Any, AsyncGenerator, Dict, List


class SSEEventManager:
    """
    Centralized SSE connection management and event broadcasting.

    Manages multiple SSE connections and broadcasts events to all connected clients.
    Uses bounded queues to prevent memory issues with slow clients.
    """

    def __init__(self, max_queue_size: int = 100) -> None:
        self._max_queue_size = max_queue_size
        self._queues: List[asyncio.Queue] = []
        self._lock = asyncio.Lock()

    async def register(self) -> AsyncGenerator[str, None]:
        """
        Register a new client and return an async generator that yields SSE strings.
        """
        queue: asyncio.Queue = asyncio.Queue(maxsize=self._max_queue_size)
        async with self._lock:
            self._queues.append(queue)

        try:
            while True:
                event = await queue.get()
                yield event
        finally:
            async with self._lock:
                if queue in self._queues:
                    self._queues.remove(queue)

    async def broadcast(self, event: Dict[str, Any]) -> None:
        """
        Broadcast an event to all registered clients.
        """
        sse = self._format_sse_event(event)
        async with self._lock:
            for q in list(self._queues):
                try:
                    q.put_nowait(sse)
                except asyncio.QueueFull:
                    # Drop the oldest event to make room for the new one
                    try:
                        q.get_nowait()
                    except asyncio.QueueEmpty:
                        pass
                    q.put_nowait(sse)

    def _format_sse_event(self, event: Dict[str, Any]) -> str:
        """
        Convert an event dictionary into a properly formatted SSE string.
        """
        parts: List[str] = []

        # Optional fields
        if "event" in event:
            parts.append(f"event: {event['event']}")
        if "id" in event:
            parts.append(f"id: {event['id']}")
        if "retry" in event:
            parts.append(f"retry: {event['retry']}")

        # Data field (must be string)
        data = event.get("data", "")
        if not isinstance(data, str):
            data = json.dumps(data, default=self._json_serializer)

        # Split data into lines
        for line in data.splitlines():
            parts.append(f"data: {line}")

        # End of event
        parts.append("")
        return "\n".join(parts)

    def _json_serializer(self, obj: Any) -> Any:
        """
        Fallback serializer for objects that json.dumps cannot handle.
        """
        try:
            return str(obj)
        except Exception:
            return None