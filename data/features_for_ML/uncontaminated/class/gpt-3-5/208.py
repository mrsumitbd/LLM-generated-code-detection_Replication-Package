from typing import Any

class AsyncJobResourceWithRawResponse:

    def __init__(self, job: AsyncJobResource) -> None:
        self.job = job

    def get_job_status(self) -> str:
        return self.job.get_status()

    def get_raw_response(self) -> Any:
        return self.job.get_raw_response()