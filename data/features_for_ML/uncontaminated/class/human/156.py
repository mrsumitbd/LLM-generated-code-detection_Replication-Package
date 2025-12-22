from .actions import (
    ActionsResource,
    AsyncActionsResource,
    ActionsResourceWithRawResponse,
    AsyncActionsResourceWithRawResponse,
    ActionsResourceWithStreamingResponse,
    AsyncActionsResourceWithStreamingResponse,
)
from .snapshots import (
    SnapshotsResource,
    AsyncSnapshotsResource,
    SnapshotsResourceWithRawResponse,
    AsyncSnapshotsResourceWithRawResponse,
    SnapshotsResourceWithStreamingResponse,
    AsyncSnapshotsResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)

class VolumesResourceWithRawResponse:
    def __init__(self, volumes: VolumesResource) -> None:
        self._volumes = volumes

        self.create = to_raw_response_wrapper(
            volumes.create,
        )
        self.retrieve = to_raw_response_wrapper(
            volumes.retrieve,
        )
        self.list = to_raw_response_wrapper(
            volumes.list,
        )
        self.delete = to_raw_response_wrapper(
            volumes.delete,
        )
        self.delete_by_name = to_raw_response_wrapper(
            volumes.delete_by_name,
        )

    @cached_property
    def actions(self) -> ActionsResourceWithRawResponse:
        return ActionsResourceWithRawResponse(self._volumes.actions)

    @cached_property
    def snapshots(self) -> SnapshotsResourceWithRawResponse:
        return SnapshotsResourceWithRawResponse(self._volumes.snapshots)