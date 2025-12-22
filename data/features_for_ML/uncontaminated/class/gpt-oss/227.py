import threading
import uuid
import time
import logging
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, Tuple, Optional

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

@dataclass
class _TimerTask:
    """Internal representation of a countdown task."""
    task_id: str
    duration: float
    callback: Callable[..., Any]
    args: Tuple[Any, ...] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    start_time: float = field(default_factory=time.time)
    timer: Optional[threading.Timer] = None
    _remaining: float = field(init=False)

    def __post_init__(self):
        self._remaining = self.duration

    @property
    def remaining(self) -> float:
        """Return the remaining time in seconds."""
        if self.timer and self.timer.is_alive():
            elapsed = time.time() - self.start_time
            return max(0.0, self.duration - elapsed)
        return 0.0


class TimerService:
    """
    倒计时器服务，管理所有倒计时任务.
    """

    def __init__(self):
        self._tasks: Dict[str, _TimerTask] = {}
        self._lock = threading.Lock()

    def add_task(
        self,
        duration: float,
        callback: Callable[..., Any],
        args: Tuple[Any, ...] = (),
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        添加一个倒计时任务。

        :param duration: 倒计时秒数
        :param callback: 计时结束时调用的函数
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: 任务 ID
        """
        if kwargs is None:
            kwargs = {}
        task_id = str(uuid.uuid4())
        task = _TimerTask(
            task_id=task_id,
            duration=duration,
            callback=callback,
            args=args,
            kwargs=kwargs,
        )

        def _wrapper():
            try:
                callback(*args, **kwargs)
            except Exception as exc:
                _logger.exception("Timer task %s raised an exception", task_id)
            finally:
                self._remove_task(task_id)

        timer = threading.Timer(duration, _wrapper)
        task.timer = timer

        with self._lock:
            self._tasks[task_id] = task
        timer.start()
        _logger.debug("Added timer task %s with duration %.2f", task_id, duration)
        return task_id

    def cancel_task(self, task_id: str) -> bool:
        """
        取消指定的倒计时任务。

        :param task_id: 任务 ID
        :return: 是否成功取消
        """
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                _logger.warning("Attempted to cancel non-existent task %s", task_id)
                return False
            if task.timer and task.timer.is_alive():
                task.timer.cancel()
            del self._tasks[task_id]
        _logger.debug("Cancelled timer task %s", task_id)
        return True

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        获取指定任务的详细信息。

        :param task_id: 任务 ID
        :return: 任务信息字典或 None
        """
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return None
            return {
                "task_id": task.task_id,
                "duration": task.duration,
                "remaining": task.remaining,
                "callback": task.callback,
                "args": task.args,
                "kwargs": task.kwargs,
            }

    def list_tasks(self) -> Dict[str, Dict[str, Any]]:
        """
        列出所有正在运行的倒计时任务。

        :return: 任务 ID 到任务信息的映射
        """
        with self._lock:
            return {tid: self.get_task(tid) for tid in self._tasks}

    def get_remaining(self, task_id: str) -> Optional[float]:
        """
        获取指定任务剩余时间。

        :param task_id: 任务 ID
        :return: 剩余秒数或 None
        """
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return None
            return task.remaining

    def _remove_task(self, task_id: str) -> None:
        """
        内部方法：任务完成后从字典中移除。
        """
        with self._lock:
            self._tasks.pop(task_id, None)
        _logger.debug("Removed timer task %s after completion", task_id)

    def shutdown(self) -> None:
        """
        关闭服务，取消所有正在运行的任务。
        """
        with self._lock:
            task_ids = list(self._tasks.keys())
        for tid in task_ids:
            self.cancel_task(tid)
        _logger.info("TimerService shutdown: all tasks cancelled")