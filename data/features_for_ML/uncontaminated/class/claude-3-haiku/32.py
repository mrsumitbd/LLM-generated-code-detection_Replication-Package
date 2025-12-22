from typing import Dict

class LabelInfo:
    """Information about a label"""

    def __init__(self, label_id: str, label_name: str, label_description: str):
        self.label_id = label_id
        self.label_name = label_name
        self.label_description = label_description

    def to_dict(self) -> Dict[str, str]:
        return {
            "label_id": self.label_id,
            "label_name": self.label_name,
            "label_description": self.label_description
        }