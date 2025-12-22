import time
import threading

class PresenceUpdater:
    """Manages continuous presence updates for WhatsApp conversations."""

    def __init__(self, sender, recipient: str, presence_type: str = "composing"):
        self.sender = sender
        self.recipient = recipient
        self.presence_type = presence_type
        self.running = False
        self.presence_thread = None

    def start(self):
        self.running = True
        self.presence_thread = threading.Thread(target=self._presence_loop)
        self.presence_thread.start()

    def stop(self):
        self.running = False
        if self.presence_thread:
            self.presence_thread.join()

    def mark_message_sent(self):
        self.stop()

    def _presence_loop(self):
        while self.running:
            self.sender.send_presence_update(self.recipient, self.presence_type)
            time.sleep(3)