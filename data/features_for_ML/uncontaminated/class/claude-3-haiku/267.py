from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class Property:
    name: str
    required: bool
    value: Any

class PropertyList:
    """
    属性列表.
    """

    def __init__(self, properties: Optional[List[Property]] = None):
        self.properties = properties or []

    def add_property(self, prop: Property):
        self.properties.append(prop)

    def __getitem__(self, name: str) -> Property:
        for prop in self.properties:
            if prop.name == name:
                return prop
        raise KeyError(f"Property '{name}' not found.")

    def get_required(self) -> List[str]:
        return [prop.name for prop in self.properties if prop.required]

    def to_json(self) -> Dict[str, Any]:
        return {prop.name: prop.value for prop in self.properties}

    def parse_arguments(self, arguments: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not arguments:
            return {}

        parsed = {}
        for prop in self.properties:
            if prop.name in arguments:
                parsed[prop.name] = arguments[prop.name]
            elif prop.required:
                raise ValueError(f"Required property '{prop.name}' is missing.")
        return parsed