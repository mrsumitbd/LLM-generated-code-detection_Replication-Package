from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, ClassVar, Dict, Optional

class ThreadMessage:
    """
    Represents a message to be added to a thread.
    """

    type: str
    content: Dict[str, Any]
    is_llm_message: bool = False
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[float] = field(
        default_factory=lambda: datetime.now().timestamp()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary for API calls"""
        return {
            "type": self.type,
            "content": self.content,
            "is_llm_message": self.is_llm_message,
            "metadata": self.metadata or {},
            "timestamp": self.timestamp,
        }