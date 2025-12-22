class PropertyGroupInfo:
    """Property group information"""

    def __init__(self, group_id: str = None, group_name: str = None, properties: List[Dict[str, Any]] = None):
        self.group_id = group_id
        self.group_name = group_name
        self.properties = properties or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'properties': self.properties
        }