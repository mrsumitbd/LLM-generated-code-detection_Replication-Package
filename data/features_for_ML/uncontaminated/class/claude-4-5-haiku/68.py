import asyncio
import threading
from pathlib import Path
from typing import Callable, Optional


class AsyncLogLoader:
    """异步日志加载器"""

    def __init__(self, callback):
        self.callback = callback
        self._loading = False
        self._thread = None
        self._loop = None

    def load_file_async(self, file_path, progress_callback=None):
        if self._loading:
            return
        
        self._loading = True
        self._thread = threading.Thread(
            target=self._load_file_thread,
            args=(file_path, progress_callback),
            daemon=True
        )
        self._thread.start()

    def _load_file_thread(self, file_path, progress_callback=None):
        try:
            path = Path(file_path)
            if not path.exists():
                self.callback(None, f"File not found: {file_path}")
                return
            
            file_size = path.stat().st_size
            lines = []
            bytes_read = 0
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if not self._loading:
                        break
                    
                    lines.append(line.rstrip('\n'))
                    bytes_read += len(line.encode('utf-8'))
                    
                    if progress_callback and file_size > 0:
                        progress = (bytes_read / file_size) * 100
                        progress_callback(progress)
            
            if self._loading:
                self.callback(lines, None)
            else:
                self.callback(None, "Loading stopped")
        
        except Exception as e:
            self.callback(None, str(e))
        finally:
            self._loading = False

    def stop_loading(self):
        self._loading = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)