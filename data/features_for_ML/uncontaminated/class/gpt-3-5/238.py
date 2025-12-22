from typing import Any
from async_snapshots_resource import AsyncSnapshotsResource

class AsyncSnapshotsResourceWithRawResponse:

    def __init__(self, snapshots: AsyncSnapshotsResource) -> None:
        self.snapshots = snapshots

    async def get_snapshot(self, snapshot_id: str) -> Any:
        return await self.snapshots.get_snapshot(snapshot_id)

    async def create_snapshot(self, data: Any) -> Any:
        return await self.snapshots.create_snapshot(data)

    async def delete_snapshot(self, snapshot_id: str) -> Any:
        return await self.snapshots.delete_snapshot(snapshot_id)