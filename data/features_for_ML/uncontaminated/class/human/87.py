from abc import abstractmethod
import asyncio

class AsyncTask:
    """异步任务基类"""

    def __init__(self, task_name: str | None = None, wait_before_start: int = 0, run_interval: int = 0):
        self.task_name: str = task_name or self.__class__.__name__
        """任务名称"""

        self.wait_before_start: int = wait_before_start
        """运行任务前是否进行等待（单位：秒，设为0则不等待）"""

        self.run_interval: int = run_interval
        """多次运行的时间间隔（单位：秒，设为0则仅运行一次）"""

    @abstractmethod
    async def run(self):
        """
        任务的执行过程
        """
        pass

    async def start_task(self, abort_flag: asyncio.Event):
        if self.wait_before_start > 0:
            # 等待指定时间后开始任务
            await asyncio.sleep(self.wait_before_start)

        while not abort_flag.is_set():
            await self.run()
            if self.run_interval > 0:
                await asyncio.sleep(self.run_interval)
            else:
                break