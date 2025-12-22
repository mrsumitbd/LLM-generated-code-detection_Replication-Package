from typing import Dict, Any

class ActionInfo:
    """Complete action information with binding support"""

    def __init__(self, action_id: str, action_name: str, action_description: str, action_type: str, action_parameters: Dict[str, Any]):
        self.action_id = action_id
        self.action_name = action_name
        self.action_description = action_description
        self.action_type = action_type
        self.action_parameters = action_parameters

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "action_name": self.action_name,
            "action_description": self.action_description,
            "action_type": self.action_type,
            "action_parameters": self.action_parameters
        }