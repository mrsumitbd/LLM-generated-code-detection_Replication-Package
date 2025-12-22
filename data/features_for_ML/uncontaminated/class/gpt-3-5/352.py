from typing import Optional, FrameType

class MatchingService:

    def __init__(self) -> None:
        pass

    def _get_job_runner(self) -> JobRunner:
        pass

    def handle_sigterm(self, _: int, __: Optional[FrameType]) -> None:
        pass

    def handle_sigint(self, _: int, __: Optional[FrameType]) -> None:
        pass

    def get_available_jobs_count(self) -> int:
        pass

    def run_next_job(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass