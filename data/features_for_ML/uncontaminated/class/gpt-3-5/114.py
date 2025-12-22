class Message:
    """A single message in a conversation."""

    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

    def __str__(self):
        return f"{self.sender}: {self.content}"