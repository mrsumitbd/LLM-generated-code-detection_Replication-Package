from cached_property import cached_property

class VolumesResourceWithRawResponse:
    def __init__(self, volumes: VolumesResource) -> None:
        self._volumes = volumes

    @cached_property
    def actions(self) -> ActionsResourceWithRawResponse:
        return ActionsResourceWithRawResponse(self._volumes.actions)

    @cached_property
    def snapshots(self) -> SnapshotsResourceWithRawResponse:
        return SnapshotsResourceWithRawResponse(self._volumes.snapshots)