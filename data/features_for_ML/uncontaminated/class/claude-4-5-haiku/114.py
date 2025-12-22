from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Message:
    """A single message in a conversation."""
    
    content: str
    role: str = "user"
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.content:
            raise ValueError("Message content cannot be empty")
        if self.role not in ("user", "assistant", "system"):
            raise ValueError(f"Invalid role: {self.role}")
        if not isinstance(self.metadata, dict):
            self.metadata = {}
    
    def __str__(self) -> str:
        return f"{self.role}: {self.content}"
    
    def __repr__(self) -> str:
        return f"Message(content={self.content!r}, role={self.role!r}, timestamp={self.timestamp!r})"
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "role": self.role,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        if isinstance(data.get("timestamp"), str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)