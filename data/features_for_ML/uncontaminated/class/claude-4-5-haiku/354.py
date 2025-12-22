class RuleContext:
    """Represents context information for values referenced in conditions."""

    def __init__(self, **kwargs):
        self._context = kwargs

    def to_dict(self) -> dict[str, str]:
        return dict(self._context)