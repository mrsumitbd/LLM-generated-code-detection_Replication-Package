class ErrorReport:
    """Information on a parsing failure."""

    def __init__(self, error_type, error_message):
        self.error_type = error_type
        self.error_message = error_message

    def __str__(self) -> str:
        return f"Error Type: {self.error_type}, Error Message: {self.error_message}"