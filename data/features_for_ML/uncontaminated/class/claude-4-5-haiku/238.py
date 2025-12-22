class AsyncSnapshotsResourceWithRawResponse:

    def __init__(self, snapshots: AsyncSnapshotsResource) -> None:
        self._snapshots = snapshots

    @property
    def list(self) -> Callable[..., Awaitable[BinaryIO]]:
        return self._snapshots.list

    @property
    def retrieve(self) -> Callable[..., Awaitable[BinaryIO]]:
        return self._snapshots.retrieve

    @property
    def create(self) -> Callable[..., Awaitable[BinaryIO]]:
        return self._snapshots.create

    @property
    def delete(self) -> Callable[..., Awaitable[BinaryIO]]:
        return self._snapshots.delete

    @property
    def update(self) -> Callable[..., Awaitable[BinaryIO]]:
        return self._snapshots.update