import time
import threading

class PresenceUpdater:
    """Manages continuous presence updates for WhatsApp conversations."""

    def __init__(self, sender, recipient: str, presence_type: str = "composing"):
        """
        Initialize the presence updater.

        Args:
            sender: EvolutionApiSender instance
            recipient: WhatsApp ID to send presence to
            presence_type: Type of presence status
        """
        self.sender = sender
        self.recipient = recipient
        self.presence_type = presence_type
        self.should_update = False
        self.update_thread = None
        self.message_sent = False

    def start(self):
        """Start sending continuous presence updates."""
        if self.update_thread and self.update_thread.is_alive():
            # Already running
            return

        self.should_update = True
        self.message_sent = False
        self.update_thread = threading.Thread(target=self._presence_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
        logger.info(f"Started presence updates for {self.recipient}")

    def stop(self):
        """Stop sending presence updates."""
        self.should_update = False
        self.message_sent = True

        # Send one more presence update with "paused" to clear the typing indicator
        try:
            self.sender.send_presence(self.recipient, "paused", 1)
        except Exception as e:
            logger.debug(f"Error clearing presence: {e}")

        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1.0)

        logger.info(f"Stopped presence updates for {self.recipient}")

    def mark_message_sent(self):
        """Mark that the message has been sent, but keep typing indicator for a short time."""
        self.message_sent = True

    def _presence_loop(self):
        """Thread method to continuously update presence."""
        # Initial delay before starting presence updates
        time.sleep(0.5)

        time.time()
        post_send_cooldown = 1.0  # Short cooldown after message sent (in seconds)
        message_sent_time = None

        while self.should_update:
            try:
                # Send presence update with a 15-second refresh
                self.sender.send_presence(self.recipient, self.presence_type, 15)

                # If message was sent, start the post-send cooldown
                if self.message_sent and message_sent_time is None:
                    message_sent_time = time.time()

                # Check if we've reached the post-send cooldown time
                if message_sent_time and (time.time() - message_sent_time > post_send_cooldown):
                    logger.info("Typing indicator cooldown completed after message sent")
                    self.should_update = False
                    break

                # Normal refresh cycle (shorter now for responsiveness)
                for _ in range(5):  # 5 second refresh cycle
                    if not self.should_update:
                        break
                    time.sleep(1)

            except Exception as e:
                logger.error(f"Error updating presence: {e}")
                # Wait a bit before retrying
                time.sleep(2)