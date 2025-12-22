import threading
import time
from typing import Optional, Callable


class PresenceUpdater:
    """Manages continuous presence updates for WhatsApp conversations."""

    def __init__(self, sender, recipient: str, presence_type: str = "composing"):
        self.sender = sender
        self.recipient = recipient
        self.presence_type = presence_type
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._stop_event = threading.Event()
        self._last_update_time = 0
        self._update_interval = 5  # seconds

    def start(self):
        """Start sending presence updates."""
        if self._running:
            return
        
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._presence_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop sending presence updates."""
        if not self._running:
            return
        
        self._running = False
        self._stop_event.set()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def mark_message_sent(self):
        """Mark that a message has been sent and stop presence updates."""
        self.stop()

    def _presence_loop(self):
        """Continuously send presence updates at regular intervals."""
        while self._running and not self._stop_event.is_set():
            try:
                current_time = time.time()
                
                # Send presence update
                if hasattr(self.sender, 'send_presence'):
                    self.sender.send_presence(
                        self.recipient,
                        self.presence_type
                    )
                
                self._last_update_time = current_time
                
                # Wait for the next update interval or until stop is called
                self._stop_event.wait(timeout=self._update_interval)
                
            except Exception:
                # Continue on error
                if self._stop_event.wait(timeout=1):
                    break