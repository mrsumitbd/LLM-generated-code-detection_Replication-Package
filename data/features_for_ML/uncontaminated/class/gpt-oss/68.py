import asyncio
import os
from typing import Callable, Optional


class AsyncLogLoader:
    """异步日志加载器"""

    def __init__(self, callback: Callable[[str], None]):
        """
        :param callback: 处理每一行日志的回调函数，接收一行字符串
        """
        self._callback = callback
        self._progress_callback: Optional[Callable[[float], None]] = None
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()
        self._loop = asyncio.get_event_loop()

    async def _load(self, file_path: str, progress_callback: Optional[Callable[[float], None]]):
        """
        内部协程，负责读取文件并调用回调
        """
        self._progress_callback = progress_callback
        total_size = os.path.getsize(file_path)
        read_bytes = 0

        # 使用 to_thread 让阻塞 I/O 在后台线程执行
        async with asyncio.to_thread(open, file_path, "r", encoding="utf-8") as f:
            # 逐行读取
            for line in f:
                if self._stop_event.is_set():
                    break

                # 调用行回调
                if self._callback:
                    # 让回调在事件循环中执行，避免跨线程问题
                    self._loop.call_soon_threadsafe(self._callback, line.rstrip("\n"))

                read_bytes += len(line.encode("utf-8"))
                if self._progress_callback:
                    percent = read_bytes / total_size if total_size else 0
                    self._loop.call_soon_threadsafe(self._progress_callback, percent)

        # 读取完成或被停止后，清理状态
        self._task = None
        self._stop_event.clear()

    def load_file_async(self, file_path: str, progress_callback: Optional[Callable[[float], None]] = None):
        """
        开始异步加载日志文件

        :param file_path: 日志文件路径
        :param progress_callback: 进度回调，接收 0.0-1.0 的浮点数
        :return: asyncio.Task 对象
        """
        if self._task and not self._task.done():
            raise RuntimeError("A loading task is already running.")
        self._task = self._loop.create_task(self._load(file_path, progress_callback))
        return self._task

    def stop_loading(self):
        """
        立即停止正在进行的日志加载
        """
        if self._task and not self._task.done():
            self._stop_event.set()
            # 取消任务以释放资源
            self._task.cancel()