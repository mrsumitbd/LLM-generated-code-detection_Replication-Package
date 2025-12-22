from functools import cached_property

class VolumesResourceWithRawResponse:

    def __init__(self, volumes: VolumesResource) -> None:
        self.volumes = volumes

    @cached_property
    def actions(self) -> ActionsResourceWithRawResponse:
        return ActionsResourceWithRawResponse(self.volumes.actions)

    @cached_property
    def snapshots(self) -> SnapshotsResourceWithRawResponse:
        return SnapshotsResourceWithRawResponse(self.volumes.snapshots)