from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncJobResourceWithRawResponse:
    def __init__(self, job: AsyncJobResource) -> None:
        self._job = job

        self.cancel = async_to_raw_response_wrapper(
            job.cancel,
        )
        self.get = async_to_raw_response_wrapper(
            job.get,
        )
        self.get_all = async_to_raw_response_wrapper(
            job.get_all,
        )