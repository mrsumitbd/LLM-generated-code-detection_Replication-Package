from typing import Dict

class LabelInfo:
    """Information about a label"""

    def __init__(self, name: str = "", value: str = ""):
        self.name = name
        self.value = value

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "value": self.value
        }