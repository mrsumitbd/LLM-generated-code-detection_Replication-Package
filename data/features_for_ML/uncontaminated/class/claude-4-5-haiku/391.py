class ActionParameterInfo:
    """Information about an action parameter"""

    def __init__(self, name: str, param_type: str, required: bool = False, default: Any = None, description: str = ""):
        self.name = name
        self.param_type = param_type
        self.required = required
        self.default = default
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.param_type,
            "required": self.required,
            "default": self.default,
            "description": self.description
        }