import asyncio
import threading
from typing import Optional


class _AsyncLoopManager:
    """一个管理后台asyncio事件循环的单例。"""

    _instance: Optional["_AsyncLoopManager"] = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                # 初始化成员
                cls._instance._loop: Optional[asyncio.AbstractEventLoop] = None
                cls._instance._thread: Optional[threading.Thread] = None
                cls._instance._started = False
            return cls._instance

    def get_loop(self) -> asyncio.AbstractEventLoop:
        """返回后台事件循环，若未启动则启动。"""
        if not self._started:
            self._start_loop()
        return self._loop

    def _start_loop(self):
        """启动后台线程和事件循环。"""
        if self._started:
            return
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop, name="AsyncLoopThread", daemon=True
        )
        self._thread.start()
        # 等待循环真正启动
        while not self._loop.is_running():
            pass
        self._started = True

    def _run_loop(self):
        """后台线程运行事件循环。"""
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_forever()
        finally:
            self._loop.close()

    def shutdown(self):
        """优雅关闭后台事件循环和线程。"""
        if not self._started:
            return
        # 让循环停止
        self._loop.call_soon_threadsafe(self._loop.stop)
        # 等待线程结束
        self._thread.join()
        self._started = False
        self._loop = None
        self._thread = None