class ActionInfo:
    """Complete action information with binding support"""

    def __init__(self, action_id: str = "", action_type: str = "", 
                 description: str = "", parameters: Dict[str, Any] = None,
                 bindings: Dict[str, Any] = None, metadata: Dict[str, Any] = None):
        self.action_id = action_id
        self.action_type = action_type
        self.description = description
        self.parameters = parameters or {}
        self.bindings = bindings or {}
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "description": self.description,
            "parameters": self.parameters,
            "bindings": self.bindings,
            "metadata": self.metadata
        }

    def __repr__(self) -> str:
        return f"ActionInfo(action_id={self.action_id!r}, action_type={self.action_type!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ActionInfo):
            return False
        return (self.action_id == other.action_id and
                self.action_type == other.action_type and
                self.description == other.description and
                self.parameters == other.parameters and
                self.bindings == other.bindings and
                self.metadata == other.metadata)