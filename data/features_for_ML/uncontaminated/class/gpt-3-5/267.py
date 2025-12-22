from typing import List, Optional, Dict, Any

class Property:
    pass

class PropertyList:
    """
    属性列表.
    """

    def __init__(self, properties: Optional[List[Property]] = None):
        self.properties = properties if properties is not None else []

    def add_property(self, prop: Property):
        self.properties.append(prop)

    def __getitem__(self, name: str) -> Property:
        for prop in self.properties:
            if prop.name == name:
                return prop
        raise KeyError(f"Property '{name}' not found")

    def get_required(self) -> List[str]:
        required_props = [prop.name for prop in self.properties if prop.required]
        return required_props

    def to_json(self) -> Dict[str, Any]:
        properties_json = [prop.to_json() for prop in self.properties]
        return {"properties": properties_json}

    def parse_arguments(self, arguments: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        parsed_args = {}
        for prop in self.properties:
            if prop.name in arguments:
                parsed_args[prop.name] = prop.parse_value(arguments[prop.name])
        return parsed_args