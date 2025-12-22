from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

class LabelInfo:
    """Information about a label"""

    id: str
    language: str
    value: str

    def to_dict(self) -> Dict[str, str]:
        return {"id": self.id, "language": self.language, "value": self.value}