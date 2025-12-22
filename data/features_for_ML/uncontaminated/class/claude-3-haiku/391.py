from typing import Dict, Any

class ActionParameterInfo:
    """Information about an action parameter"""

    def __init__(self, name: str, description: str, required: bool, data_type: str):
        self.name = name
        self.description = description
        self.required = required
        self.data_type = data_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "data_type": self.data_type
        }