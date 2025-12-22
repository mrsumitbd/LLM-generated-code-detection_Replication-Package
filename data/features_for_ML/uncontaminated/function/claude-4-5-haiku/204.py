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
    import re
    
    if not task_id:
        raise ValueError("task_id cannot be empty")
    
    if len(task_id) > 255:
        raise ValueError("task_id is too long (max 255 characters)")
    
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', task_id):
        raise ValueError("task_id contains invalid characters")
    
    if '..' in task_id or task_id.startswith('.'):
        raise ValueError("task_id contains invalid path traversal patterns")
    
    return task_id