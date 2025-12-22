
class Skip:
    """Indicates that this was intentially skipped."""

    message: str | None
    location: str | None

    def __init__(self, message: str | None = None, location: str | None = None):
        self.message = message
        self.location = location

    def combine(self, other: Outcome):
        if isinstance(other, (DepSkip,)):
            return self

        return other

    def __str__(self) -> str:
        if self.message:
            return f"Skip (message={self.message})"

        return "User Skip"