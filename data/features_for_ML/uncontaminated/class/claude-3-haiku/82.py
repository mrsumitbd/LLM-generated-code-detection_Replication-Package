import rust
from typing import Any

class WorkerResourcesInternal:
    pass

class WorkerGroup:

    @classmethod
    def make(cls, id: str, stage_name: str, allocations: list[WorkerResourcesInternal]) -> 'WorkerGroup':
        worker_group = cls(rust.WorkerGroup())
        worker_group._id = id
        worker_group._stage_name = stage_name
        worker_group._allocations = allocations
        return worker_group

    def __init__(self, rust_worker: rust.WorkerGroup):
        self._rust_worker = rust_worker

    @property
    def id(self) -> str:
        return self._id

    @property
    def stage_name(self) -> str:
        return self._stage_name

    @property
    def allocations(self) -> list[WorkerResourcesInternal]:
        return self._allocations

    @property
    def rust(self) -> rust.WorkerGroup:
        return self._rust_worker

    def split_allocation_per_gpu(self) -> list[WorkerResourcesInternal]:
        return [allocation.split_per_gpu() for allocation in self._allocations]

    def __reduce__(self) -> Any:
        return self._reconstruct, (str(self),)

    @classmethod
    def _reconstruct(cls, serialized: str) -> 'WorkerGroup':
        # Implement the logic to reconstruct the WorkerGroup from the serialized string
        pass

    def __hash__(self) -> int:
        return hash((self._id, self._stage_name, tuple(self._allocations)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WorkerGroup):
            return False
        return (self._id, self._stage_name, tuple(self._allocations)) == (other._id, other._stage_name, tuple(other._allocations))

    def __repr__(self) -> str:
        return f"WorkerGroup(id={self._id}, stage_name={self._stage_name}, allocations={self._allocations})"

    def __str__(self) -> str:
        return f"WorkerGroup(id={self._id}, stage_name={self._stage_name})"