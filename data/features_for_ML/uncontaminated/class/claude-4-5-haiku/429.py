class ToolCall:
    """Represents a single tool call with id + function field."""

    def __init__(self, call_id: str, function: ToolFunction):
        self.id = call_id
        self.function = function

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "function": self.function.to_dict() if hasattr(self.function, 'to_dict') else self.function
        }

    def get(self, key: str, default: Any = None) -> Any:
        if key == "id":
            return self.id
        elif key == "function":
            return self.function
        return default

    def __getitem__(self, key: str) -> Any:
        if key == "id":
            return self.id
        elif key == "function":
            return self.function
        raise KeyError(key)