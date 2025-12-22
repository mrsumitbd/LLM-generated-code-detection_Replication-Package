
class RuleContext:
    """Represents context information for values referenced in conditions."""

    fact_attribute: str
    value: str

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for YAML serialization."""
        return {self.fact_attribute: self.value}