class Skip:
    """Indicates that this was intentially skipped."""

    def __init__(self, message: str | None = None, location: str | None = None):
        self.message = message
        self.location = location

    def combine(self, other: Outcome):
        if isinstance(other, Skip):
            return Skip(
                message=self.message or other.message,
                location=self.location or other.location
            )
        return other

    def __str__(self) -> str:
        if self.message:
            return f"Skip: {self.message}"
        return "Skip"