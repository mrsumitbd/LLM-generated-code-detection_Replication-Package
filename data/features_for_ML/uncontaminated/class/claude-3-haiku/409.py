import asyncio
import threading

class _AsyncLoopManager:
    """一个管理后台asyncio事件循环的单例。"""

    _instance = None
    _loop = None
    _loop_thread = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_AsyncLoopManager, cls).__new__(cls)
            cls._loop = asyncio.new_event_loop()
            cls._loop_thread = threading.Thread(target=cls._run_loop, daemon=True)
            cls._loop_thread.start()
        return cls._instance

    def get_loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def shutdown(self):
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._loop_thread.join()