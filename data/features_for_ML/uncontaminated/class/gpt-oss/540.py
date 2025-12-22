from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


@dataclass
class PropertyGroupInfo:
    """Property group information"""

    group_name: str = ""
    group_description: str = ""
    properties: List[Any] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)