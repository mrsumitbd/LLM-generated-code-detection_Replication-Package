class ErrorReport:
    """Information on a parsing failure."""

    def __init__(
        self,
        message: str,
        line: int | None = None,
        column: int | None = None,
        context: str | None = None,
    ) -> None:
        self.message = message
        self.line = line
        self.column = column
        self.context = context

    def __str__(self) -> str:
        parts = [f"Error: {self.message}"]
        if self.line is not None:
            parts.append(f"Line {self.line}")
        if self.column is not None:
            parts.append(f"Column {self.column}")
        if self.context:
            parts.append(f"Context: {self.context}")
        return " | ".join(parts)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"line={self.line!r}, "
            f"column={self.column!r}, "
            f"context={self.context!r})"
        )