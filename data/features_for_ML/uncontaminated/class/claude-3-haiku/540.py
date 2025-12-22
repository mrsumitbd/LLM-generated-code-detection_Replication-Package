from typing import Dict, Any

class PropertyGroupInfo:
    """Property group information"""

    def __init__(self, group_id: str, group_name: str, properties: Dict[str, Any]):
        self.group_id = group_id
        self.group_name = group_name
        self.properties = properties

    def to_dict(self) -> Dict[str, Any]:
        return {
            "group_id": self.group_id,
            "group_name": self.group_name,
            "properties": self.properties
        }