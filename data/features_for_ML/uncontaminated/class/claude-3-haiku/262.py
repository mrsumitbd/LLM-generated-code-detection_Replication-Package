import concurrent.futures
import os
from typing import Callable

from tts2face.config import Tts2FaceConfigModel


class LiteAvatarWorkerManager:
    def __init__(self, concurrent_limit: int, handler_root: str, config: Tts2FaceConfigModel):
        self.concurrent_limit = concurrent_limit
        self.handler_root = handler_root
        self.config = config
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrent_limit)
        self.tasks = []

    def start_worker(self, task: Callable):
        future = self.executor.submit(task)
        self.tasks.append(future)

    def destroy(self):
        self.executor.shutdown(wait=True)
        for task in self.tasks:
            task.cancel()
        os.rmdir(self.handler_root)