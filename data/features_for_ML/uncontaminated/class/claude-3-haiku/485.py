from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ModelArgs:
    name: str
    params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError("'name' must be a string")
        if not isinstance(self.params, dict):
            raise TypeError("'params' must be a dictionary")

    @classmethod
    def from_name(cls, name: str):
        return cls(name=name)