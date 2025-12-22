from typing import Dict, Any, Optional

class QueueManager:
    """Task queue manager to ensure only one task executes at a time"""

    def __init__(self):
        self.task_queue = []
        self.task_status = {}

    def add_task(self, task_id: str, user_info: Dict) -> int:
        self.task_queue.append(task_id)
        self.task_status[task_id] = {'user_info': user_info, 'status': 'pending'}
        return len(self.task_queue)

    def get_next_task(self) -> Optional[str]:
        if self.task_queue:
            return self.task_queue[0]
        return None

    def complete_task(self, task_id: str, result: Any = None, error: Any = None):
        if task_id in self.task_status:
            self.task_status[task_id]['status'] = 'completed' if result else 'failed'
            self.task_status[task_id]['result'] = result
            self.task_status[task_id]['error'] = error
            self.task_queue.pop(0)

    def get_queue_position(self, task_id: str) -> int:
        if task_id in self.task_queue:
            return self.task_queue.index(task_id) + 1
        return -1

    def get_task_status(self, task_id: str) -> Dict:
        return self.task_status.get(task_id, {})