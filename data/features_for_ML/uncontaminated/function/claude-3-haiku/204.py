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
    if len(task_id) > 100:
        raise ValueError("Task ID cannot be longer than 100 characters.")

    if not re.match(r'^[a-zA-Z0-9_-]+$', task_id):
        raise ValueError("Task ID can only contain alphanumeric characters, underscores, and hyphens.")

    return task_id