class TodoItem:
    """Represents a single TODO item found in the codebase."""
    
    def __init__(self, file_path: str, line_number: int, content: str, priority: str = "normal"):
        """
        Initialize a TodoItem.
        
        Args:
            file_path: Path to the file containing the TODO
            line_number: Line number where the TODO is located
            content: The TODO comment text
            priority: Priority level of the TODO (low, normal, high)
        """
        self.file_path = file_path
        self.line_number = line_number
        self.content = content
        self.priority = priority
    
    def __repr__(self) -> str:
        """Return a string representation of the TodoItem."""
        return f"TodoItem(file_path='{self.file_path}', line_number={self.line_number}, content='{self.content}', priority='{self.priority}')"
    
    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return f"{self.file_path}:{self.line_number} [{self.priority}] {self.content}"
    
    def __eq__(self, other) -> bool:
        """Check equality with another TodoItem."""
        if not isinstance(other, TodoItem):
            return False
        return (self.file_path == other.file_path and 
                self.line_number == other.line_number and 
                self.content == other.content and 
                self.priority == other.priority)
    
    def __hash__(self) -> int:
        """Return hash of the TodoItem."""
        return hash((self.file_path, self.line_number, self.content, self.priority))
    
    def to_dict(self) -> dict:
        """Convert TodoItem to a dictionary."""
        return {
            "file_path": self.file_path,
            "line_number": self.line_number,
            "content": self.content,
            "priority": self.priority
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        """Create a TodoItem from a dictionary."""
        return cls(
            file_path=data.get("file_path", ""),
            line_number=data.get("line_number", 0),
            content=data.get("content", ""),
            priority=data.get("priority", "normal")
        )