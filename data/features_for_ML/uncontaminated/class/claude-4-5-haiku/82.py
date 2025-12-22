class WorkerGroup:

    @classmethod
    def make(cls, id: str, stage_name: str, allocations: list[WorkerResourcesInternal]) -> WorkerGroup:
        rust_allocations = [alloc.rust for alloc in allocations]
        rust_worker_group = rust.WorkerGroup.make(id, stage_name, rust_allocations)
        return cls(rust_worker_group)

    def __init__(self, rust_worker: rust.WorkerGroup):
        self._rust_worker = rust_worker

    @property
    def id(self) -> str:
        return self._rust_worker.id

    @property
    def stage_name(self) -> str:
        return self._rust_worker.stage_name

    @property
    def allocations(self) -> list[WorkerResourcesInternal]:
        return [WorkerResourcesInternal(alloc) for alloc in self._rust_worker.allocations]

    @property
    def rust(self) -> rust.WorkerGroup:
        return self._rust_worker

    def split_allocation_per_gpu(self) -> list[WorkerResourcesInternal]:
        rust_allocations = self._rust_worker.split_allocation_per_gpu()
        return [WorkerResourcesInternal(alloc) for alloc in rust_allocations]

    def __reduce__(self) -> Any:
        serialized = self._rust_worker.serialize()
        return (self._reconstruct, (serialized,))

    @classmethod
    def _reconstruct(cls, serialized: str) -> WorkerGroup:
        rust_worker_group = rust.WorkerGroup.deserialize(serialized)
        return cls(rust_worker_group)

    def __hash__(self) -> int:
        return hash((self.id, self.stage_name, tuple(self.allocations)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WorkerGroup):
            return False
        return (self.id == other.id and 
                self.stage_name == other.stage_name and 
                self.allocations == other.allocations)

    def __repr__(self) -> str:
        return f"WorkerGroup(id={self.id!r}, stage_name={self.stage_name!r}, allocations={self.allocations!r})"

    def __str__(self) -> str:
        return f"WorkerGroup(id={self.id}, stage_name={self.stage_name}, allocations={self.allocations})"