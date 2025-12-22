import asyncio

class _AsyncLoopManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(_AsyncLoopManager, cls).__new__(cls)
            cls._instance._loop = asyncio.get_event_loop()
            cls._instance._loop_thread = None
        return cls._instance

    def get_loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    def _run_loop(self):
        self._loop.run_forever()

    def shutdown(self):
        self._loop.stop()