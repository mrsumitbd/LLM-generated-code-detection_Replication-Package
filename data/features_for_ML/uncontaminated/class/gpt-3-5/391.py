class ActionParameterInfo:
    """Information about an action parameter"""

    def __init__(self, name: str, data_type: str, required: bool):
        self.name = name
        self.data_type = data_type
        self.required = required

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'data_type': self.data_type,
            'required': self.required
        }