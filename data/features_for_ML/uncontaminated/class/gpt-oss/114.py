from __future__ import annotations

import datetime
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Message:
    """A single message in a conversation."""

    sender: str
    content: str
    timestamp: Optional[datetime.datetime] = None
    message_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.sender, str) or not self.sender:
            raise ValueError("sender must be a non-empty string")
        if not isinstance(self.content, str) or not self.content:
            raise ValueError("content must be a non-empty string")
        if self.timestamp is None:
            self.timestamp = datetime.datetime.utcnow()
        elif not isinstance(self.timestamp, datetime.datetime):
            raise TypeError("timestamp must be a datetime instance or None")
        if self.message_id is None:
            self.message_id = f"{self.sender}-{int(self.timestamp.timestamp() * 1000)}"
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dict")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "message_id": self.message_id,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        timestamp = data.get("timestamp")
        if timestamp is not None:
            timestamp = datetime.datetime.fromisoformat(timestamp)
        return cls(
            sender=data["sender"],
            content=data["content"],
            timestamp=timestamp,
            message_id=data.get("message_id"),
            metadata=data.get("metadata", {}),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __str__(self) -> str:
        return f"[{self.timestamp.isoformat()}] {self.sender}: {self.content}"