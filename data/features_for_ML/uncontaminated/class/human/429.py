from typing import Any, Dict, List, Optional

class ToolCall:
    """Represents a single tool call with id + function field."""

    def __init__(self, call_id: str, function: ToolFunction):
        self.id = call_id
        self.function = function

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "function": self.function.to_dict()}

    # Provide dict-like access for downstream hooks expecting Chat-style dicts
    def get(self, key: str, default: Any = None) -> Any:
        if key == "id":
            return self.id
        if key == "function":
            return self.function
        return default

    def __getitem__(self, key: str) -> Any:
        val = self.get(key)
        if val is None:
            raise KeyError(key)
        return val