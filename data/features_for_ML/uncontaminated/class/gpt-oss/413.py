import threading
import time
import datetime
from typing import Callable, Any, Dict, Tuple, Optional


class SchedulerService:
    """Service for managing scheduled tasks and automatic execution"""

    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._condition = threading.Condition(self._lock)
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def start(self) -> None:
        """Start the scheduler worker thread."""
        with self._lock:
            if self._running:
                return
            self._running = True
            self._worker_thread = threading.Thread(
                target=self._worker, name="SchedulerWorker", daemon=True
            )
            self._worker_thread.start()

    def stop(self) -> None:
        """Stop the scheduler worker thread."""
        with self._lock:
            if not self._running:
                return
            self._running = False
            self._condition.notify_all()
        if self._worker_thread:
            self._worker_thread.join()
            self._worker_thread = None

    def schedule_once(
        self,
        name: str,
        func: Callable,
        delay_seconds: float,
        args: Tuple[Any, ...] = (),
        kwargs: Dict[str, Any] = {},
    ) -> None:
        """Schedule a one‑time task to run after a delay."""
        run_at = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
        self._add_task(name, func, run_at, None, args, kwargs)

    def schedule_at(
        self,
        name: str,
        func: Callable,
        run_at: datetime.datetime,
        args: Tuple[Any, ...] = (),
        kwargs: Dict[str, Any] = {},
    ) -> None:
        """Schedule a one‑time task to run at a specific datetime."""
        self._add_task(name, func, run_at, None, args, kwargs)

    def schedule_every(
        self,
        name: str,
        func: Callable,
        interval_seconds: float,
        args: Tuple[Any, ...] = (),
        kwargs: Dict[str, Any] = {},
    ) -> None:
        """Schedule a recurring task that runs every interval_seconds."""
        run_at = datetime.datetime.now() + datetime.timedelta(seconds=interval_seconds)
        self._add_task(name, func, run_at, interval_seconds, args, kwargs)

    def cancel_task(self, name: str) -> None:
        """Cancel a scheduled task."""
        with self._lock:
            self._tasks.pop(name, None)

    def get_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Return a copy of the current tasks dictionary."""
        with self._lock:
            return {k: v.copy() for k, v in self._tasks.items()}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _add_task(
        self,
        name: str,
        func: Callable,
        run_at: datetime.datetime,
        interval: Optional[float],
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ) -> None:
        with self._lock:
            self._tasks[name] = {
                "func": func,
                "run_at": run_at,
                "interval": interval,
                "args": args,
                "kwargs": kwargs,
            }
            self._condition.notify_all()

    def _worker(self) -> None:
        while True:
            with self._lock:
                if not self._running:
                    break

                now = datetime.datetime.now()
                # Find the next task to run
                next_task_name, next_task = None, None
                min_delta = None
                for name, task in self._tasks.items():
                    delta = (task["run_at"] - now).total_seconds()
                    if delta < 0:
                        delta = 0
                    if min_delta is None or delta < min_delta:
                        min_delta = delta
                        next_task_name = name
                        next_task = task

                if next_task is None:
                    # No tasks scheduled; wait until a new task is added
                    self._condition.wait()
                    continue

                # Wait until the next task is due or a new task is added
                if min_delta > 0:
                    self._condition.wait(timeout=min_delta)
                    continue

                # Time to run the task
                task_to_run = self._tasks.pop(next_task_name, None)
                if task_to_run is None:
                    continue

            # Run the task outside the lock
            threading.Thread(
                target=self._run_task,
                args=(next_task_name, task_to_run),
                daemon=True,
            ).start()

    def _run_task(self, name: str, task: Dict[str, Any]) -> None:
        try:
            task["func"](*task["args"], **task["kwargs"])
        except Exception:
            # Swallow exceptions to keep the scheduler running
            pass
        finally:
            # Reschedule if it's a recurring task
            if task["interval"] is not None:
                next_run = datetime.datetime.now() + datetime.timedelta(
                    seconds=task["interval"]
                )
                with self._lock:
                    self._tasks[name] = {
                        "func": task["func"],
                        "run_at": next_run,
                        "interval": task["interval"],
                        "args": task["args"],
                        "kwargs": task["kwargs"],
                    }
                    self._condition.notify_all()

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    # ------------------------------------------------------------------
    # Destructor
    # ------------------------------------------------------------------
    def __del__(self):
        self.stop()