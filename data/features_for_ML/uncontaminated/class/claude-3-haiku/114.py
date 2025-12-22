class Message:
    """A single message in a conversation."""

    def __init__(self, sender: str, recipient: str, text: str, timestamp: float):
        self.sender = sender
        self.recipient = recipient
        self.text = text
        self.timestamp = timestamp

    def __post_init__(self):
        if not isinstance(self.sender, str) or not self.sender:
            raise ValueError("Sender must be a non-empty string")
        if not isinstance(self.recipient, str) or not self.recipient:
            raise ValueError("Recipient must be a non-empty string")
        if not isinstance(self.text, str) or not self.text:
            raise ValueError("Text must be a non-empty string")
        if not isinstance(self.timestamp, float) or self.timestamp < 0:
            raise ValueError("Timestamp must be a non-negative float")

    def __str__(self):
        return f"{self.sender} sent to {self.recipient} at {self.timestamp}: {self.text}"

    def __repr__(self):
        return f"Message(sender='{self.sender}', recipient='{self.recipient}', text='{self.text}', timestamp={self.timestamp})"