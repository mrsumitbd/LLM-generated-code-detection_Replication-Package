import threading
import time

class AsyncLogLoader:
    """异步日志加载器"""

    def __init__(self, callback):
        self.callback = callback
        self.loading_thread = None
        self.stop_flag = False

    def load_file_async(self, file_path, progress_callback=None):
        self.stop_flag = False
        self.loading_thread = threading.Thread(target=self._load_file, args=(file_path, progress_callback))
        self.loading_thread.start()

    def stop_loading(self):
        self.stop_flag = True

    def _load_file(self, file_path, progress_callback):
        # Simulating file loading progress
        for i in range(1, 101):
            if self.stop_flag:
                break
            time.sleep(0.1)  # Simulating file loading time
            if progress_callback:
                progress_callback(i)
        if not self.stop_flag:
            self.callback("File loaded successfully")
        else:
            self.callback("File loading stopped")

# Example usage:
def progress_callback(progress):
    print(f"Loading progress: {progress}%")

def callback(message):
    print(message)

loader = AsyncLogLoader(callback)
loader.load_file_async("example.log", progress_callback)
time.sleep(2)  # Allowing some time for loading
loader.stop_loading()