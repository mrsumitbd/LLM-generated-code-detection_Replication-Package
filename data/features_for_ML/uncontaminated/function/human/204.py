import re
from utils.be_config import (
    ALLOWED_EXTENSIONS,
    ALLOWED_MIME_TYPES,
    DANGEROUS_PATTERNS,
    MAX_FILE_SIZE,
    MAX_FILENAME_LENGTH,
    MAX_TASK_ID_LENGTH,
    TASK_ID_PATTERN,
)

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
    if not task_id:
        raise ValueError("Task ID is required")

    if len(task_id) > MAX_TASK_ID_LENGTH:
        raise ValueError(f"Task ID too long (max {MAX_TASK_ID_LENGTH} characters)")

    # Check for directory traversal patterns
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, task_id):
            raise ValueError(f"Task ID contains invalid characters: {pattern}")

    # Ensure task_id matches allowed pattern
    if not re.match(TASK_ID_PATTERN, task_id):
        raise ValueError(
            "Task ID must contain only alphanumeric characters, hyphens, and underscores"
        )

    return task_id