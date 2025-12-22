from typing import Any, Dict


class ToolCall:
    """Represents a single tool call with id + function field."""

    def __init__(self, call_id: str, function: "ToolFunction"):
        self.id = call_id
        self.function = function

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the tool call."""
        return {
            "id": self.id,
            "function": self.function.to_dict() if hasattr(self.function, "to_dict") else self.function,
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the tool call dictionary."""
        return self.to_dict().get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-like access to the tool call."""
        return self.get(key)