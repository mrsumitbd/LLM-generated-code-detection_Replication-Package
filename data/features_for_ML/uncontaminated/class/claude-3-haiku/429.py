from typing import Dict, Any

class ToolCall:
    """Represents a single tool call with id + function field."""

    def __init__(self, call_id: str, function: ToolFunction):
        self.call_id = call_id
        self.function = function
        self.data = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "call_id": self.call_id,
            "function": self.function.to_dict(),
            **self.data
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]