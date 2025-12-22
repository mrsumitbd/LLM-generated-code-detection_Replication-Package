import asyncio

class AsyncLogLoader:
    """异步日志加载器"""

    def __init__(self, callback):
        self.callback = callback
        self.task = None
        self.is_loading = False

    async def _load_file(self, file_path, progress_callback=None):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if progress_callback:
                        progress_callback(i, len(lines))
                    await asyncio.sleep(0.1)
                self.callback(lines)
        except Exception as e:
            self.callback(None, e)

    def load_file_async(self, file_path, progress_callback=None):
        if not self.is_loading:
            self.is_loading = True
            self.task = asyncio.create_task(self._load_file(file_path, progress_callback))

    def stop_loading(self):
        if self.task and not self.task.done():
            self.task.cancel()
        self.is_loading = False