from typing import Dict, Any

class BehavioralRegister:
    """Definition of a behavioral register."""

    def __init__(self, name: str, description: str, behaviors: Dict[str, float]):
        self.name = name
        self.description = description
        self.behaviors = behaviors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "behaviors": self.behaviors
        }