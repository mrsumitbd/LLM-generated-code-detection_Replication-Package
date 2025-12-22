from dataclasses import dataclass, field
from typing import Any


@dataclass
class AIRAState:
    """State object for AIRA LangGraph workflow."""
    
    query: str = ""
    context: str = ""
    response: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    messages: list[dict[str, str]] = field(default_factory=list)
    error: str | None = None
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the messages list."""
        self.messages.append({"role": role, "content": content})
    
    def set_error(self, error: str) -> None:
        """Set an error message."""
        self.error = error
    
    def clear_error(self) -> None:
        """Clear the error message."""
        self.error = None
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update metadata with a key-value pair."""
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get a metadata value by key."""
        return self.metadata.get(key, default)