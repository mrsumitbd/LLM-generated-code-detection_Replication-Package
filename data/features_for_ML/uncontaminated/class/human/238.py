from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class AsyncSnapshotsResourceWithRawResponse:
    def __init__(self, snapshots: AsyncSnapshotsResource) -> None:
        self._snapshots = snapshots

        self.create = async_to_raw_response_wrapper(
            snapshots.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            snapshots.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            snapshots.list,
        )
        self.delete = async_to_raw_response_wrapper(
            snapshots.delete,
        )