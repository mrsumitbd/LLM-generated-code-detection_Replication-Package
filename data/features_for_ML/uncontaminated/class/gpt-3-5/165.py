from typing import Dict, Any

class ThreadMessage:
    """
    Represents a message to be added to a thread.
    """

    def __init__(self, message: str, author: str):
        self.message = message
        self.author = author

    def to_dict(self) -> Dict[str, Any]:
        return {
            'message': self.message,
            'author': self.author
        }