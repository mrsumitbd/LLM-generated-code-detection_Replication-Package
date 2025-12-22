class ErrorReport:
    """Information on a parsing failure."""

    def __init__(self, line_number: int, column_number: int, message: str):
        self.line_number = line_number
        self.column_number = column_number
        self.message = message

    def __str__(self) -> str:
        return f"Error at line {self.line_number}, column {self.column_number}: {self.message}"