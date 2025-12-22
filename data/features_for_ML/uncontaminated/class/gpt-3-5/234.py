class Skip:
    """Indicates that this was intentionally skipped."""

    def __init__(self, message: str | None = None, location: str | None = None):
        self.message = message
        self.location = location

    def combine(self, other: 'Skip') -> 'Skip':
        return Skip(message=self.message + other.message if self.message and other.message else None,
                    location=self.location + other.location if self.location and other.location else None)

    def __str__(self) -> str:
        return f"Skip: {self.message} at {self.location}" if self.message and self.location else "Skip"