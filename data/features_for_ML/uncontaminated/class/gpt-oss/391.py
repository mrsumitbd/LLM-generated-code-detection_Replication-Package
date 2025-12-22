from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class ActionParameterInfo:
    """Information about an action parameter"""

    name: str
    type: str
    description: Optional[str] = None
    default: Any = None
    required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the parameter info."""
        data = asdict(self)
        # Omit keys whose values are None for a cleaner output
        return {k: v for k, v in data.items() if v is not None}