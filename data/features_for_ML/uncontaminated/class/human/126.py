from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

class TaskStats:
    """Performance statistics for a task"""

    task_id: str
    status: TaskStatus
    created_at: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    execution_time_ms: Optional[float] = None
    memory_usage_mb: Optional[float] = None
    retries: int = 0
    worker_id: Optional[int] = None