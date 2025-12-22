from typing import Dict

class LabelInfo:
    """Information about a label"""

    def __init__(self, **kwargs):
        self._data = kwargs

    def to_dict(self) -> Dict[str, str]:
        return {k: str(v) for k, v in self._data.items()}