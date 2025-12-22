from typing import Dict, Any

class ThreadMessage:
    """
    Represents a message to be added to a thread.
    """

    def __init__(self, message_id: str, author: str, content: str, timestamp: float) -> None:
        self.message_id = message_id
        self.author = author
        self.content = content
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "author": self.author,
            "content": self.content,
            "timestamp": self.timestamp
        }