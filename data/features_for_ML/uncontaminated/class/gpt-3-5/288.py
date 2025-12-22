class ActionInfo:
    """Complete action information with binding support"""

    def __init__(self, action_name: str, action_type: str, action_params: Dict[str, Any]):
        self.action_name = action_name
        self.action_type = action_type
        self.action_params = action_params

    def to_dict(self) -> Dict[str, Any]:
        return {
            'action_name': self.action_name,
            'action_type': self.action_type,
            'action_params': self.action_params
        }