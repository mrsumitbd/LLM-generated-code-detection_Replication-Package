class Skip:
    """Indicates that this was intentially skipped."""

    def __init__(self, message: str | None = None, location: str | None = None):
        self.message = message
        self.location = location

    def combine(self, other: 'Outcome'):
        if isinstance(other, Skip):
            if self.message is None:
                self.message = other.message
            if self.location is None:
                self.location = other.location
        return self

    def __str__(self) -> str:
        if self.message is None and self.location is None:
            return "Skipped"
        elif self.message is None:
            return f"Skipped at {self.location}"
        elif self.location is None:
            return f"Skipped: {self.message}"
        else:
            return f"Skipped: {self.message} at {self.location}"