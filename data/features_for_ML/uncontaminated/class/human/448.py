from typing import Dict, Any, List, Optional

class BehavioralRegister:
    """Definition of a behavioral register."""
    name: str
    offset: int
    behavior: BehaviorType
    default_value: int = 0x00000000
    pattern: Optional[str] = None
    counter_bits: Optional[int] = None
    description: str = ""
    read_only: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to template-compatible dictionary."""
        result = {
            "offset": self.offset,
            "behavior": self.behavior.value,
            "default": self.default_value,
            "description": self.description,
            "read_only": self.read_only
        }
        if self.pattern:
            result["pattern"] = self.pattern
        if self.counter_bits:
            result["counter_bits"] = self.counter_bits
        return result