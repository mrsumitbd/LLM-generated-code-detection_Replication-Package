import queue
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from threading import Lock

class QueueManager:
    """Task queue manager to ensure only one task executes at a time"""
    
    def __init__(self):
        self.current_task: Optional[str] = None
        self.task_queue: queue.Queue = queue.Queue()
        self.task_status: Dict[str, Dict] = {}
        self.lock = Lock()
    
    def add_task(self, task_id: str, user_info: Dict) -> int:
        """Add task to queue, return queue position"""
        with self.lock:
            self.task_status[task_id] = {
                "status": "queued",
                "created_at": datetime.now(),
                "user_info": user_info,
                "result": None,
                "error": None
            }
            self.task_queue.put(task_id)
            return self.task_queue.qsize()
    
    def get_next_task(self) -> Optional[str]:
        """Get next task to execute"""
        with self.lock:
            if self.current_task is None and not self.task_queue.empty():
                task_id = self.task_queue.get()
                self.current_task = task_id
                self.task_status[task_id]["status"] = "running"
                self.task_status[task_id]["started_at"] = datetime.now()
                return task_id
            return None
    
    def complete_task(self, task_id: str, result: Any = None, error: Any = None):
        """Mark task as completed"""
        with self.lock:
            if task_id in self.task_status:
                self.task_status[task_id]["status"] = "completed" if result else "failed"
                self.task_status[task_id]["completed_at"] = datetime.now()
                self.task_status[task_id]["result"] = result
                self.task_status[task_id]["error"] = error
            if self.current_task == task_id:
                self.current_task = None
    
    def get_queue_position(self, task_id: str) -> int:
        """Get task position in queue"""
        with self.lock:
            if task_id == self.current_task:
                return 0  # Currently executing
            
            queue_list = list(self.task_queue.queue)
            try:
                return queue_list.index(task_id) + 1
            except ValueError:
                return -1  # Task not in queue
    
    def get_task_status(self, task_id: str) -> Dict:
        """Get task status"""
        with self.lock:
            return self.task_status.get(task_id, {"status": "not_found"})