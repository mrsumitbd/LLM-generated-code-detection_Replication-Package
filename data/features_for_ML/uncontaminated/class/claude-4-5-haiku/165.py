from typing import Dict, Any, Optional

class ThreadMessage:
    """
    Represents a message to be added to a thread.
    """

    def __init__(
        self,
        role: str,
        content: str,
        file_ids: Optional[list] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.role = role
        self.content = content
        self.file_ids = file_ids or []
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "role": self.role,
            "content": self.content,
        }
        
        if self.file_ids:
            result["file_ids"] = self.file_ids
        
        if self.metadata:
            result["metadata"] = self.metadata
        
        return result