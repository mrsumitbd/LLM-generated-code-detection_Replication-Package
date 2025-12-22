class TodoItem:
    """Represents a single TODO item found in the codebase."""
    
    def __init__(self, description, priority=1, completed=False):
        self.description = description
        self.priority = priority
        self.completed = completed
        
    def mark_as_completed(self):
        self.completed = True
        
    def update_priority(self, new_priority):
        self.priority = new_priority
        
    def __str__(self):
        return f"Description: {self.description}, Priority: {self.priority}, Completed: {self.completed}"