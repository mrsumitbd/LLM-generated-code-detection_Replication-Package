import time
from typing import Callable, Dict

class TimerService:
    """
    倒计时器服务，管理所有倒计时任务.
    """

    def __init__(self):
        self.tasks: Dict[str, Callable[[], None]] = {}
        self.start_times: Dict[str, float] = {}
        self.durations: Dict[str, float] = {}

    def start_timer(self, task_id: str, duration: float, callback: Callable[[], None]) -> None:
        """
        启动一个新的倒计时任务.

        Args:
            task_id (str): 任务的唯一标识符.
            duration (float): 倒计时的持续时间(秒).
            callback (Callable[[], None]): 倒计时结束时要执行的回调函数.
        """
        self.tasks[task_id] = callback
        self.start_times[task_id] = time.time()
        self.durations[task_id] = duration

    def check_timers(self) -> None:
        """
        检查所有正在进行的倒计时任务,如果有任务已经结束,则执行相应的回调函数.
        """
        for task_id, start_time in self.start_times.items():
            duration = self.durations[task_id]
            if time.time() - start_time >= duration:
                self.tasks[task_id]()
                del self.tasks[task_id]
                del self.start_times[task_id]
                del self.durations[task_id]