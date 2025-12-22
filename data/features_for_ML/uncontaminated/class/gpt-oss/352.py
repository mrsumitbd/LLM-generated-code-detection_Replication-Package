import signal
import threading
import queue
from typing import Optional, FrameType, Callable


class JobRunner:
    """A simple job runner that executes callables from a queue."""

    def __init__(self) -> None:
        self._jobs = queue.Queue()
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def add_job(self, job: Callable[[], None]) -> None:
        """Add a callable job to the queue."""
        self._jobs.put(job)

    def get_available_jobs_count(self) -> int:
        """Return the number of jobs waiting to be processed."""
        return self._jobs.qsize()

    def run_next_job(self) -> None:
        """Run the next job in the queue, if any."""
        if not self._jobs.empty():
            job = self._jobs.get()
            job()

    def start(self) -> None:
        """Start the background worker thread."""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()

    def _worker(self) -> None:
        """Background worker that processes jobs."""
        while self._running:
            try:
                job = self._jobs.get(timeout=0.5)
                job()
            except queue.Empty:
                continue

    def stop(self) -> None:
        """Stop the background worker thread."""
        self._running = False
        if self._thread:
            self._thread.join()
            self._thread = None


class MatchingService:
    """Service that manages job execution and graceful shutdown."""

    def __init__(self) -> None:
        self._job_runner: Optional[JobRunner] = None
        self._original_sigterm: Optional[signal.Signals] = None
        self._original_sigint: Optional[signal.Signals] = None

    def _get_job_runner(self) -> JobRunner:
        if self._job_runner is None:
            self._job_runner = JobRunner()
        return self._job_runner

    def handle_sigterm(self, _: int, __: Optional[FrameType]) -> None:
        self.stop()

    def handle_sigint(self, _: int, __: Optional[FrameType]) -> None:
        self.stop()

    def get_available_jobs_count(self) -> int:
        return self._get_job_runner().get_available_jobs_count()

    def run_next_job(self) -> None:
        self._get_job_runner().run_next_job()

    def start(self) -> None:
        self._original_sigterm = signal.getsignal(signal.SIGTERM)
        self._original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGTERM, self.handle_sigterm)
        signal.signal(signal.SIGINT, self.handle_sigint)
        self._get_job_runner().start()

    def stop(self) -> None:
        self._get_job_runner().stop()
        if self._original_sigterm is not None:
            signal.signal(signal.SIGTERM, self._original_sigterm)
        if self._original_sigint is not None:
            signal.signal(signal.SIGINT, self._original_sigint)