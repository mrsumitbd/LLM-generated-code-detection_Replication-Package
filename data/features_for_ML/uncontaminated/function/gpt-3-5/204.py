def validate_task_id(task_id: str) -> str:
    if not task_id.isalnum() or len(task_id) > 50:
        raise ValueError("Invalid task_id")
    
    return task_id