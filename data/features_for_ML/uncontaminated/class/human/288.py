from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

class ActionInfo:
    """Complete action information with binding support"""

    name: str
    binding_kind: ODataBindingKind = ODataBindingKind.BOUND_TO_ENTITY_SET
    entity_name: Optional[str] = None  # For bound actions (public entity name)
    entity_set_name: Optional[str] = (
        None  # For bound actions (entity set name for OData URLs)
    )
    parameters: List["ActionParameterInfo"] = field(default_factory=list)
    return_type: Optional["ActionReturnTypeInfo"] = None
    field_lookup: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "binding_kind": self.binding_kind,  # StrEnum automatically serializes as string
            "entity_name": self.entity_name,
            "entity_set_name": self.entity_set_name,
            "parameters": [param.to_dict() for param in self.parameters],
            "return_type": self.return_type.to_dict() if self.return_type else None,
            "field_lookup": self.field_lookup,
        }