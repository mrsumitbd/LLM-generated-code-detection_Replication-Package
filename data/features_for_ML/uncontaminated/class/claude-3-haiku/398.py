from typing import Dict, Optional, Any
from collections import deque

class QueueManager:
    """Task queue manager to ensure only one task executes at a time"""

    def __init__(self):
        self.task_queue = deque()
        self.task_status = {}

    def add_task(self, task_id: str, user_info: Dict) -> int:
        self.task_queue.append(task_id)
        self.task_status[task_id] = {'user_info': user_info, 'status': 'pending'}
        return len(self.task_queue)

    def get_next_task(self) -> Optional[str]:
        if self.task_queue:
            return self.task_queue.popleft()
        return None

    def complete_task(self, task_id: str, result: Any = None, error: Any = None):
        if task_id in self.task_status:
            if error is None:
                self.task_status[task_id]['status'] = 'completed'
                self.task_status[task_id]['result'] = result
            else:
                self.task_status[task_id]['status'] = 'failed'
                self.task_status[task_id]['error'] = error

    def get_queue_position(self, task_id: str) -> int:
        if task_id in self.task_queue:
            return self.task_queue.index(task_id)
        return -1

    def get_task_status(self, task_id: str) -> Dict:
        if task_id in self.task_status:
            return self.task_status[task_id]
        return {}