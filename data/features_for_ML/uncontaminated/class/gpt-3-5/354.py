class RuleContext:
    """Represents context information for values referenced in conditions."""

    def __init__(self):
        self.context = {}

    def to_dict(self) -> dict[str, str]:
        return self.context

    def add_context(self, key: str, value: str):
        self.context[key] = value

    def remove_context(self, key: str):
        if key in self.context:
            del self.context[key]