from typing import Dict, Any, Optional
from collections import deque
import time


class QueueManager:
    """Task queue manager to ensure only one task executes at a time"""

    def __init__(self):
        # Queue of task IDs in FIFO order
        self._queue: deque[str] = deque()
        # Mapping from task ID to task metadata
        self._tasks: Dict[str, Dict[str, Any]] = {}
        # Currently running task ID (None if idle)
        self._running_task: Optional[str] = None

    def add_task(self, task_id: str, user_info: Dict) -> int:
        """
        Add a new task to the queue.

        :param task_id: Unique identifier for the task.
        :param user_info: Dictionary containing user-related information.
        :return: The position of the task in the queue (1‑based).
        """
        if task_id in self._tasks:
            raise ValueError(f"Task ID '{task_id}' already exists.")
        now = time.time()
        self._tasks[task_id] = {
            "user_info": user_info,
            "status": "queued",
            "result": None,
            "error": None,
            "timestamp": now,
        }
        self._queue.append(task_id)
        return len(self._queue)  # 1‑based position

    def get_next_task(self) -> Optional[str]:
        """
        Retrieve the next task ID to run if no task is currently running.

        :return: Task ID or None if no task is available or a task is running.
        """
        if self._running_task is not None:
            return None
        if not self._queue:
            return None
        next_task_id = self._queue.popleft()
        task = self._tasks[next_task_id]
        task["status"] = "running"
        self._running_task = next_task_id
        return next_task_id

    def complete_task(self, task_id: str, result: Any = None, error: Any = None):
        """
        Mark the specified task as completed or failed.

        :param task_id: ID of the task to complete.
        :param result: Result of the task (if successful).
        :param error: Error information (if failed).
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task ID '{task_id}' not found.")
        task = self._tasks[task_id]
        if self._running_task != task_id:
            raise RuntimeError(f"Task '{task_id}' is not currently running.")
        if error is not None:
            task["status"] = "failed"
            task["error"] = error
        else:
            task["status"] = "completed"
            task["result"] = result
        self._running_task = None

    def get_queue_position(self, task_id: str) -> int:
        """
        Get the current position of a task in the queue.

        :param task_id: ID of the task.
        :return: Position (1‑based) if queued, 0 if running, -1 if completed or not found.
        """
        if task_id not in self._tasks:
            return -1
        if self._running_task == task_id:
            return 0
        try:
            idx = list(self._queue).index(task_id)
            return idx + 1  # 1‑based
        except ValueError:
            # Task is not in the queue (likely completed)
            return -1

    def get_task_status(self, task_id: str) -> Dict:
        """
        Retrieve the status dictionary for a task.

        :param task_id: ID of the task.
        :return: Dictionary containing status, result, error, user_info, and timestamp.
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task ID '{task_id}' not found.")
        task = self._tasks[task_id]
        return {
            "status": task["status"],
            "result": task["result"],
            "error": task["error"],
            "user_info": task["user_info"],
            "timestamp": task["timestamp"],
        }