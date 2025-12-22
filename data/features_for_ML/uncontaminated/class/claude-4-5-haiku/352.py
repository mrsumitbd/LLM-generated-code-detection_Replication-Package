import signal
from typing import Optional, FrameType
from queue import Queue
from threading import Thread, Event

class JobRunner:
    def run(self) -> None:
        pass

class MatchingService:

    def __init__(self) -> None:
        self._job_queue: Queue = Queue()
        self._running: Event = Event()
        self._worker_thread: Optional[Thread] = None

    def _get_job_runner(self) -> JobRunner:
        return JobRunner()

    def handle_sigterm(self, _: int, __: Optional[FrameType]) -> None:
        self.stop()

    def handle_sigint(self, _: int, __: Optional[FrameType]) -> None:
        self.stop()

    def get_available_jobs_count(self) -> int:
        return self._job_queue.qsize()

    def run_next_job(self) -> None:
        if not self._job_queue.empty():
            job_runner = self._job_queue.get()
            job_runner.run()

    def start(self) -> None:
        self._running.set()
        signal.signal(signal.SIGTERM, self.handle_sigterm)
        signal.signal(signal.SIGINT, self.handle_sigint)
        
        self._worker_thread = Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def stop(self) -> None:
        self._running.clear()
        if self._worker_thread is not None:
            self._worker_thread.join(timeout=5)

    def _worker_loop(self) -> None:
        while self._running.is_set():
            self.run_next_job()