class ErrorReport:
    """Information on a parsing failure."""

    def __init__(self, line: int, column: int, message: str):
        self.line = line
        self.column = column
        self.message = message

    def __str__(self) -> str:
        return f"Line {self.line}, Column {self.column}: {self.message}"