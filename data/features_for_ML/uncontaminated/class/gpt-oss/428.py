import threading
import time
from typing import Any


class SchedulerService:
    """Background service that monitors and publishes scheduled posts"""

    def __init__(self, scheduler: Any):
        """
        Initialize the service with a scheduler instance.

        :param scheduler: An object that provides `get_due_posts()` and `publish(post)` methods.
        """
        self.scheduler = scheduler
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        """
        Background loop that checks for due posts and publishes them.
        """
        while not self._stop_event.is_set():
            try:
                due_posts = self.scheduler.get_due_posts()
            except Exception:
                due_posts = []

            for post in due_posts:
                try:
                    self.scheduler.publish(post)
                except Exception:
                    # Log or handle publish errors as needed
                    pass

            # Sleep briefly to avoid tight loop
            time.sleep(1)

    def stop(self):
        """
        Stop the background service gracefully.
        """
        self._stop_event.set()
        self._thread.join()