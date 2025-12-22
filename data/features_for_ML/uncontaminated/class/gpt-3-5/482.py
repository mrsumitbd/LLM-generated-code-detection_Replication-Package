class UpdateRoleRequest:
    """update Role request object"""

    def __init__(self, role_id: int, new_role_name: str):
        self.role_id = role_id
        self.new_role_name = new_role_name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpdateRoleRequest":
        return cls(data['role_id'], data['new_role_name'])