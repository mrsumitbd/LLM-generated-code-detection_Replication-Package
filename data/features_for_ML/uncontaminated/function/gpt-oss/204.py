import re

def validate_task_id(task_id: str) -> str:
    """
    Validate and sanitize task_id to prevent directory traversal.

    Args:
        task_id: The task ID to validate

    Returns:
        Sanitized task ID

    Raises:
        ValueError: If task_id contains invalid characters or is too long
    """
    if not isinstance(task_id, str):
        raise ValueError("task_id must be a string")

    # Strip whitespace
    task_id = task_id.strip()

    # Maximum allowed length (common filesystem limit)
    MAX_LENGTH = 255
    if len(task_id) == 0:
        raise ValueError("task_id cannot be empty")
    if len(task_id) > MAX_LENGTH:
        raise ValueError(f"task_id is too long (max {MAX_LENGTH} characters)")

    # Allowed characters: alphanumerics, hyphen, underscore, dot
    # Reject any path separators or other suspicious characters
    if not re.fullmatch(r"[A-Za-z0-9._-]+", task_id):
        raise ValueError("task_id contains invalid characters")

    # Ensure no leading/trailing dots or hyphens that could be misinterpreted
    if task_id.startswith((".", "-")) or task_id.endswith((".", "-")):
        raise ValueError("task_id cannot start or end with '.' or '-'")

    return task_id