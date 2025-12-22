from typing import Dict, Any, Optional

class UpdateRoleRequest:
    """update Role request object"""

    name: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    icon: Optional[str] = None
    is_active: Optional[bool] = None
    enable_l0_retrieval: Optional[bool] = None
    enable_l1_retrieval: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpdateRoleRequest":
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            system_prompt=data.get("system_prompt"),
            icon=data.get("icon"),
            is_active=data.get("is_active"),
            enable_l0_retrieval=data.get("enable_l0_retrieval"),
            enable_l1_retrieval=data.get("enable_l1_retrieval"),
        )