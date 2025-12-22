import threading
import time
from typing import Any


class PresenceUpdater:
    """Manages continuous presence updates for WhatsApp conversations."""

    def __init__(self, sender: Any, recipient: str, presence_type: str = "composing"):
        """
        Parameters
        ----------
        sender : Any
            Object that provides a ``send_presence(recipient, presence_type)`` method.
        recipient : str
            The WhatsApp identifier of the conversation partner.
        presence_type : str, optional
            The type of presence to send (default is ``"composing"``).
        """
        self.sender = sender
        self.recipient = recipient
        self.presence_type = presence_type

        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    def start(self):
        """Start sending presence updates in a background thread."""
        with self._lock:
            if self._thread and self._thread.is_alive():
                return  # already running
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._presence_loop, daemon=True)
            self._thread.start()

    def stop(self):
        """Stop sending presence updates."""
        with self._lock:
            self._stop_event.set()
            if self._thread:
                self._thread.join()
                self._thread = None

    def mark_message_sent(self):
        """
        Call this method when a message has been sent to stop further presence updates.
        """
        self.stop()

    def _presence_loop(self):
        """
        Internal loop that sends presence updates until stopped.
        The default interval is 5 seconds, which is a reasonable compromise
        between responsiveness and network load for WhatsApp.
        """
        interval = 5.0  # seconds
        while not self._stop_event.is_set():
            try:
                self.sender.send_presence(self.recipient, self.presence_type)
            except Exception:
                # Silently ignore failures to avoid crashing the thread.
                pass
            # Wait for the interval or until stop is requested.
            self._stop_event.wait(interval)