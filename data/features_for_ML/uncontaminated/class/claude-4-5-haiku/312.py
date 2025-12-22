from collections import deque
from datetime import datetime
from typing import Any
import json
import uuid


class SSEEventManager:
    """
    Centralized SSE connection management and event broadcasting.

    Manages multiple SSE connections and broadcasts events to all connected clients.
    Uses bounded queues to prevent memory issues with slow clients.
    """

    def __init__(self, max_queue_size: int = 100) -> None:
        self.max_queue_size = max_queue_size
        self.clients: dict[str, deque] = {}
        self.client_lock = __import__('threading').Lock()

    def _format_sse_event(self, event: dict[str, Any]) -> str:
        """Format an event dictionary into SSE format."""
        lines = []
        
        if 'id' in event:
            lines.append(f"id: {event['id']}")
        
        if 'event' in event:
            lines.append(f"event: {event['event']}")
        
        if 'data' in event:
            data = event['data']
            if isinstance(data, dict):
                data = json.dumps(data, default=self._json_serializer)
            elif not isinstance(data, str):
                data = json.dumps(data, default=self._json_serializer)
            
            for line in data.split('\n'):
                lines.append(f"data: {line}")
        
        if 'retry' in event:
            lines.append(f"retry: {event['retry']}")
        
        lines.append('')
        lines.append('')
        
        return '\n'.join(lines)

    def _json_serializer(self, obj: Any) -> Any:
        """JSON serializer for objects not serializable by default json code."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        raise TypeError(f"Type {type(obj)} not serializable")

    def register_client(self) -> str:
        """Register a new SSE client and return its unique ID."""
        client_id = str(uuid.uuid4())
        with self.client_lock:
            self.clients[client_id] = deque(maxlen=self.max_queue_size)
        return client_id

    def unregister_client(self, client_id: str) -> None:
        """Unregister an SSE client."""
        with self.client_lock:
            self.clients.pop(client_id, None)

    def broadcast_event(self, event: dict[str, Any]) -> None:
        """Broadcast an event to all connected clients."""
        with self.client_lock:
            for client_queue in self.clients.values():
                try:
                    client_queue.append(event)
                except Exception:
                    pass

    def get_client_events(self, client_id: str) -> list[str]:
        """Get all pending events for a client and clear the queue."""
        with self.client_lock:
            if client_id not in self.clients:
                return []
            
            client_queue = self.clients[client_id]
            events = []
            
            while client_queue:
                event = client_queue.popleft()
                formatted_event = self._format_sse_event(event)
                events.append(formatted_event)
            
            return events

    def has_pending_events(self, client_id: str) -> bool:
        """Check if a client has pending events."""
        with self.client_lock:
            if client_id not in self.clients:
                return False
            return len(self.clients[client_id]) > 0

    def get_connected_clients_count(self) -> int:
        """Get the number of currently connected clients."""
        with self.client_lock:
            return len(self.clients)