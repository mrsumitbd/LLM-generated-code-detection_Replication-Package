class RuleContext:
    """Represents context information for values referenced in conditions."""

    def __init__(self, data: dict[str, str]):
        self._data = data

    def to_dict(self) -> dict[str, str]:
        return self._data.copy()