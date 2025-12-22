from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4


@dataclass
class ThreadMessage:
    """
    Represents a message to be added to a thread.
    """

    content: str
    author: str
    message_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the ThreadMessage instance into a dictionary suitable for
        serialization or transmission.

        Returns:
            A dictionary containing the message's data.
        """
        return {
            "message_id": self.message_id,
            "content": self.content,
            "author": self.author,
            "timestamp": self.timestamp.isoformat() + "Z",
        }