from typing import Any

class WorkerGroup:

    @classmethod
    def make(cls, id: str, stage_name: str, allocations: list[WorkerResourcesInternal]) -> WorkerGroup:
        pass

    def __init__(self, rust_worker: rust.WorkerGroup):
        pass

    @property
    def id(self) -> str:
        pass

    @property
    def stage_name(self) -> str:
        pass

    @property
    def allocations(self) -> list[WorkerResourcesInternal]:
        pass

    @property
    def rust(self) -> rust.WorkerGroup:
        pass

    def split_allocation_per_gpu(self) -> list[WorkerResourcesInternal]:
        pass

    def __reduce__(self) -> Any:
        pass

    @classmethod
    def _reconstruct(cls, serialized: str) -> WorkerGroup:
        pass

    def __hash__(self) -> int:
        pass

    def __eq__(self, other: object) -> bool:
        pass

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        pass