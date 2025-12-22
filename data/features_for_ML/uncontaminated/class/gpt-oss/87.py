import asyncio
import logging
from typing import Optional, Awaitable, Callable


class AsyncTask:
    """异步任务基类"""

    def __init__(
        self,
        task_name: Optional[str] = None,
        wait_before_start: int = 0,
        run_interval: int = 0,
    ):
        self.task_name = task_name or self.__class__.__name__
        self.wait_before_start = wait_before_start
        self.run_interval = run_interval
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()
        self._running = False

    async def run(self) -> Awaitable[None]:
        """
        子类需要重写此方法，定义任务的具体逻辑。
        """
        raise NotImplementedError("Subclasses must implement the run method")

    async def _task_loop(self) -> None:
        if self.wait_before_start > 0:
            await asyncio.sleep(self.wait_before_start)
        while not self._stop_event.is_set():
            try:
                await self.run()
            except Exception as exc:
                logging.exception(f"Exception in task {self.task_name}: {exc}")
            if self.run_interval <= 0:
                break
            await asyncio.sleep(self.run_interval)

    def start(self) -> None:
        """
        启动异步任务。若任务已在运行，则抛出异常。
        """
        if self._task is None or self._task.done():
            self._stop_event.clear()
            self._task = asyncio.create_task(self._task_loop())
            self._running = True
        else:
            raise RuntimeError(f"Task {self.task_name} is already running")

    async def stop(self) -> None:
        """
        停止异步任务。等待任务完成后返回。
        """
        if self._task and not self._task.done():
            self._stop_event.set()
            await self._task
            self._running = False

    def cancel(self) -> None:
        """
        立即取消任务。若任务已完成，则不做任何操作。
        """
        if self._task and not self._task.done():
            self._task.cancel()
            self._running = False

    @property
    def running(self) -> bool:
        return self._running

    @property
    def task(self) -> Optional[asyncio.Task]:
        return self._task

    def __repr__(self) -> str:
        status = "running" if self._running else "stopped"
        return f"<AsyncTask name={self.task_name} status={status}>"