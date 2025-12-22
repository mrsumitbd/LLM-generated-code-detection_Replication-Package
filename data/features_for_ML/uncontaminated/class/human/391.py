from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

class ActionParameterInfo:
    """Information about an action parameter"""

    name: str
    type: ActionParameterTypeInfo
    parameter_order: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.to_dict(),
            "parameter_order": self.parameter_order,
        }