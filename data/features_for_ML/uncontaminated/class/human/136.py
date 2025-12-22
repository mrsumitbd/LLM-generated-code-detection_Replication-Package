from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field

class ClientCapability:
    """Represents client capabilities."""
    roots: Optional[Dict[str, Any]] = None
    sampling: Optional[Dict[str, Any]] = None
    experimental: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to MCP format."""
        result = {}
        if self.roots is not None:
            result["roots"] = self.roots
        if self.sampling is not None:
            result["sampling"] = self.sampling
        if self.experimental:
            result["experimental"] = self.experimental
        return result