from __future__ import annotations

from typing import Any, Dict, List, Optional


class UpdateRoleRequest:
    """update Role request object"""

    def __init__(
        self,
        role_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        permissions: Optional[List[str]] = None,
    ) -> None:
        if not role_id:
            raise ValueError("role_id must be provided")
        self.role_id: str = role_id
        self.name: Optional[str] = name
        self.description: Optional[str] = description
        self.permissions: Optional[List[str]] = permissions

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpdateRoleRequest":
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        role_id = data.get("role_id")
        if role_id is None:
            raise ValueError("role_id is required in data")
        name = data.get("name")
        description = data.get("description")
        permissions = data.get("permissions")
        if permissions is not None and not isinstance(permissions, list):
            raise TypeError("permissions must be a list if provided")
        return cls(
            role_id=role_id,
            name=name,
            description=description,
            permissions=permissions,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the request."""
        result: Dict[str, Any] = {"role_id": self.role_id}
        if self.name is not None:
            result["name"] = self.name
        if self.description is not None:
            result["description"] = self.description
        if self.permissions is not None:
            result["permissions"] = self.permissions
        return result

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"role_id={self.role_id!r}, "
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"permissions={self.permissions!r})"
        )