
class TodoItem:
    """Represents a single TODO item found in the codebase."""

    file_path: str
    line_number: int
    todo_type: str  # TODO, FIXME, HACK, XXX, NOTE
    content: str
    context_lines: list[str]  # Surrounding lines for context
    author: str | None = None  # Extracted from git blame if available
    priority: str = "medium"  # low, medium, high, critical
    category: str = "general"  # general, bug, feature, refactor, docs, test
    estimated_effort: str = "unknown"  # quick, small, medium, large