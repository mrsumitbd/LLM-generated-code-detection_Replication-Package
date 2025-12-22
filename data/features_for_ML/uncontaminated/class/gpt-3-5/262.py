from typing import List

class LiteAvatarWorkerManager:

    def __init__(self, concurrent_limit: int, handler_root: str, config: Tts2FaceConfigModel):
        self.concurrent_limit = concurrent_limit
        self.handler_root = handler_root
        self.config = config
        self.workers = []

    def start_worker(self):
        if len(self.workers) < self.concurrent_limit:
            worker = LiteAvatarWorker(self.handler_root, self.config)
            worker.start()
            self.workers.append(worker)

    def destroy(self):
        for worker in self.workers:
            worker.stop()
        self.workers = []