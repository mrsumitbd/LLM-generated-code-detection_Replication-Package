from typing import Dict, Optional, Any
from collections import deque
from enum import Enum
from datetime import datetime


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class QueueManager:
    """Task queue manager to ensure only one task executes at a time"""

    def __init__(self):
        self.queue = deque()
        self.tasks = {}
        self.current_task = None

    def add_task(self, task_id: str, user_info: Dict) -> int:
        if task_id in self.tasks:
            return self.get_queue_position(task_id)
        
        self.queue.append(task_id)
        self.tasks[task_id] = {
            "task_id": task_id,
            "user_info": user_info,
            "status": TaskStatus.PENDING.value,
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None
        }
        
        return self.get_queue_position(task_id)

    def get_next_task(self) -> Optional[str]:
        if self.current_task is not None:
            return None
        
        if not self.queue:
            return None
        
        task_id = self.queue.popleft()
        self.current_task = task_id
        self.tasks[task_id]["status"] = TaskStatus.RUNNING.value
        self.tasks[task_id]["started_at"] = datetime.now().isoformat()
        
        return task_id

    def complete_task(self, task_id: str, result: Any = None, error: Any = None):
        if task_id not in self.tasks:
            return
        
        if error is not None:
            self.tasks[task_id]["status"] = TaskStatus.FAILED.value
            self.tasks[task_id]["error"] = error
        else:
            self.tasks[task_id]["status"] = TaskStatus.COMPLETED.value
            self.tasks[task_id]["result"] = result
        
        self.tasks[task_id]["completed_at"] = datetime.now().isoformat()
        
        if self.current_task == task_id:
            self.current_task = None

    def get_queue_position(self, task_id: str) -> int:
        if task_id not in self.tasks:
            return -1
        
        if self.current_task == task_id:
            return 0
        
        try:
            position = list(self.queue).index(task_id)
            return position + 1
        except ValueError:
            return -1

    def get_task_status(self, task_id: str) -> Dict:
        if task_id not in self.tasks:
            return {}
        
        task = self.tasks[task_id].copy()
        task["queue_position"] = self.get_queue_position(task_id)
        
        return task