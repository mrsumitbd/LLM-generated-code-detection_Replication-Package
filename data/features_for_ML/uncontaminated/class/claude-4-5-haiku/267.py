class PropertyList:
    """
    属性列表.
    """

    def __init__(self, properties: Optional[List[Property]] = None):
        self.properties: List[Property] = properties if properties is not None else []
        self._property_dict: Dict[str, Property] = {prop.name: prop for prop in self.properties}

    def add_property(self, prop: Property):
        self.properties.append(prop)
        self._property_dict[prop.name] = prop

    def __getitem__(self, name: str) -> Property:
        return self._property_dict[name]

    def get_required(self) -> List[str]:
        return [prop.name for prop in self.properties if prop.required]

    def to_json(self) -> Dict[str, Any]:
        return {
            "properties": {prop.name: prop.to_json() for prop in self.properties},
            "required": self.get_required()
        }

    def parse_arguments(self, arguments: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if arguments is None:
            arguments = {}
        
        result = {}
        required = self.get_required()
        
        for prop in self.properties:
            if prop.name in arguments:
                result[prop.name] = arguments[prop.name]
            elif prop.name in required:
                raise ValueError(f"Missing required property: {prop.name}")
            elif prop.default is not None:
                result[prop.name] = prop.default
        
        return result