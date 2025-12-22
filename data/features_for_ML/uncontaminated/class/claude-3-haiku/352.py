import signal
from typing import Optional, FrameType

class JobRunner:
    pass

class MatchingService:

    def __init__(self) -> None:
        self._job_runner = self._get_job_runner()
        signal.signal(signal.SIGTERM, self.handle_sigterm)
        signal.signal(signal.SIGINT, self.handle_sigint)

    def _get_job_runner(self) -> JobRunner:
        return JobRunner()

    def handle_sigterm(self, _: int, __: Optional[FrameType]) -> None:
        self.stop()

    def handle_sigint(self, _: int, __: Optional[FrameType]) -> None:
        self.stop()

    def get_available_jobs_count(self) -> int:
        return self._job_runner.get_available_jobs_count()

    def run_next_job(self) -> None:
        self._job_runner.run_next_job()

    def start(self) -> None:
        self._job_runner.start()

    def stop(self) -> None:
        self._job_runner.stop()