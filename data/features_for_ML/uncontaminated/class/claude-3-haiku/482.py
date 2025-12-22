from typing import Dict, Any

class UpdateRoleRequest:
    """update Role request object"""

    def __init__(self, role_id: str, name: str, description: str, permissions: list[str]):
        self.role_id = role_id
        self.name = name
        self.description = description
        self.permissions = permissions

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpdateRoleRequest":
        return cls(
            role_id=data["role_id"],
            name=data["name"],
            description=data["description"],
            permissions=data["permissions"]
        )