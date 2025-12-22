import time
import threading

class PresenceUpdater:
    """Manages continuous presence updates for WhatsApp conversations."""

    def __init__(self, sender, recipient: str, presence_type: str = "composing"):
        self.sender = sender
        self.recipient = recipient
        self.presence_type = presence_type
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._presence_loop).start()

    def stop(self):
        self.running = False

    def mark_message_sent(self):
        print(f"Message sent from {self.sender} to {self.recipient}")

    def _presence_loop(self):
        while self.running:
            print(f"{self.sender} is {self.presence_type} to {self.recipient}")
            time.sleep(1)

# Example usage
updater = PresenceUpdater("Alice", "Bob")
updater.start()
time.sleep(5)
updater.stop()