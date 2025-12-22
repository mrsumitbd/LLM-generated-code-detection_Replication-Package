class AsyncJobResourceWithRawResponse:
    def __init__(self, job: AsyncJobResource) -> None:
        self.job = job
        self.raw_response = None

    def get_status(self) -> AsyncJobStatus:
        return self.job.get_status()

    def get_result(self) -> Any:
        if self.raw_response is None:
            self.raw_response = self.job.get_result()
        return self.raw_response

    def cancel(self) -> None:
        self.job.cancel()