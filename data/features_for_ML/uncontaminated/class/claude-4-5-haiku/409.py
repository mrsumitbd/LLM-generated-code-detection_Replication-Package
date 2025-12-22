import asyncio
import threading
from typing import Optional

class _AsyncLoopManager:
    """一个管理后台asyncio事件循环的单例。"""
    
    _instance: Optional['_AsyncLoopManager'] = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._initialized = True
        self._start_loop()
    
    def _start_loop(self):
        """Start the event loop in a background thread."""
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        
        # Wait for loop to be ready
        while self._loop is None:
            threading.Event().wait(0.001)
    
    def get_loop(self) -> asyncio.AbstractEventLoop:
        """Get the background event loop."""
        if self._loop is None:
            raise RuntimeError("Event loop is not initialized")
        return self._loop
    
    def _run_loop(self):
        """Run the event loop in the background thread."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()
    
    def shutdown(self):
        """Shutdown the event loop and thread."""
        if self._loop is not None and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        
        if self._thread is not None:
            self._thread.join(timeout=5)
        
        self._loop = None
        self._thread = None