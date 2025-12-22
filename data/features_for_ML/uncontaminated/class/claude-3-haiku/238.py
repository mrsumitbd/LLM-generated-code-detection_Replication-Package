class AsyncSnapshotsResourceWithRawResponse:
    def __init__(self, snapshots: AsyncSnapshotsResource) -> None:
        self._snapshots = snapshots

    async def list(self, **kwargs) -> Tuple[List[Snapshot], dict]:
        response = await self._snapshots.list(**kwargs)
        return response.data, response.raw

    async def get(self, snapshot_id: str, **kwargs) -> Tuple[Snapshot, dict]:
        response = await self._snapshots.get(snapshot_id, **kwargs)
        return response.data, response.raw

    async def create(self, snapshot: Snapshot, **kwargs) -> Tuple[Snapshot, dict]:
        response = await self._snapshots.create(snapshot, **kwargs)
        return response.data, response.raw

    async def update(self, snapshot_id: str, snapshot: Snapshot, **kwargs) -> Tuple[Snapshot, dict]:
        response = await self._snapshots.update(snapshot_id, snapshot, **kwargs)
        return response.data, response.raw

    async def delete(self, snapshot_id: str, **kwargs) -> Tuple[None, dict]:
        response = await self._snapshots.delete(snapshot_id, **kwargs)
        return None, response.raw