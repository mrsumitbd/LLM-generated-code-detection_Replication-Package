class TodoItem:
    """Represents a single TODO item found in the codebase."""

    def __init__(self, file_path, line_number, description):
        self.file_path = file_path
        self.line_number = line_number
        self.description = description

    def __str__(self):
        return f"TODO in {self.file_path} at line {self.line_number}: {self.description}"

    def __eq__(self, other):
        return (
            self.file_path == other.file_path
            and self.line_number == other.line_number
            and self.description == other.description
        )

    def __hash__(self):
        return hash((self.file_path, self.line_number, self.description))