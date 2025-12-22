from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from datetime import datetime

class Message:
    """A single message in a conversation."""
    
    role: str
    content: str
    timestamp: Optional[datetime] = None
    message_index: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate message on creation."""
        if not self.role:
            raise ValueError("Message role cannot be empty")
        if self.role not in {"user", "assistant", "system", "human"}:
            # Allow common variations
            pass  # Log warning but don't fail
        if self.message_index < 0:
            raise ValueError(f"Message index cannot be negative: {self.message_index}")