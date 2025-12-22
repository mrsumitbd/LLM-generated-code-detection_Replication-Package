class ResearchAgent:
    def __init__(self, app: Any, thread: MessageThread):
        self.app = app
        self.thread = thread
        self.queue = []
        self.running = False

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.stop()

    def enqueue(self, task: Any):
        self.queue.append(task)

    def dequeue(self) -> Any:
        if self.queue:
            return self.queue.pop(0)
        return None

    def run(self):
        while self.running:
            if self.queue:
                task = self.dequeue()
                self.app.process_task(task)
            else:
                self.thread.sleep()