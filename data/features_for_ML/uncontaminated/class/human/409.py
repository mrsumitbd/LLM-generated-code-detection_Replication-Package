import asyncio
import threading
from typing import Awaitable, Callable, Dict, List, Optional, Set

class _AsyncLoopManager:
    """一个管理后台asyncio事件循环的单例。"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._loop: Optional[asyncio.AbstractEventLoop] = None
                    cls._instance._thread: Optional[threading.Thread] = None
        return cls._instance

    def get_loop(self) -> asyncio.AbstractEventLoop:
        """获取或创建在后台线程中运行的事件循环。"""
        # [修正] 使用 self 访问类属性 _lock 和实例属性 _loop, _thread
        with self._lock:
            if self._loop is None or not self._loop.is_running():
                self._loop = asyncio.new_event_loop()
                self._thread = threading.Thread(
                    target=self._run_loop, daemon=True, name="AsyncDecryptLoop"
                )
                self._thread.start()
        return self._loop

    def _run_loop(self):
        """线程的目标函数，用于运行事件循环。"""
        logger.info(f"后台事件循环线程 '{threading.current_thread().name}' 已启动。")
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()
        logger.info("后台事件循环已停止。")

    def shutdown(self):
        """同步地停止事件循环和后台线程。"""
        # [修正] 使用 self 访问类属性 _lock 和实例属性
        with self._lock:
            if self._loop and self._loop.is_running():
                self._loop.call_soon_threadsafe(self._loop.stop)
            if self._thread:
                self._thread.join()
            self._loop = None
            self._thread = None
        logger.info("后台事件循环已完全关闭。")