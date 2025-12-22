from typing import Any, Optional, Union
from cosmos_xenna._cosmos_xenna.pipelines.private.scheduling import resources as rust

class WorkerGroup:
    @classmethod
    def make(cls, id: str, stage_name: str, allocations: list[WorkerResourcesInternal]) -> WorkerGroup:
        return cls(rust.WorkerGroup(id, stage_name, [x.to_rust() for x in allocations]))

    def __init__(self, rust_worker: rust.WorkerGroup):
        self._r = rust_worker

    @property
    def id(self) -> str:
        return self._r.id

    @property
    def stage_name(self) -> str:
        return self._r.stage_name

    @property
    def allocations(self) -> list[WorkerResourcesInternal]:
        return [WorkerResourcesInternal.from_rust(x) for x in self._r.allocations]

    @property
    def rust(self) -> rust.WorkerGroup:
        return self._r

    def split_allocation_per_gpu(self) -> list[WorkerResourcesInternal]:
        """Splits the worker group's allocations into separate WorkerResources for each GPU.

        This method is useful for distributed training/inference scenarios where you need to treat
        each GPU as a separate worker with its own resource allocation. The CPUs are
        divided evenly among all GPUs in each allocation.

        Returns:
            list[WorkerResources]: A list of WorkerResources, one for each GPU in the
                worker group. Each entry contains:
                - The same node as the original allocation
                - A fraction of the CPUs (total CPUs / number of GPUs in that allocation)
                - A single GPU allocation

        Example:
            If a worker group has an allocation with 8 CPUs and 4 GPUs, this method will
            return 4 WorkerResources entries, each with 2 CPUs and 1 GPU.
        """
        return [WorkerResourcesInternal.from_rust(x) for x in self._r.split_allocation_per_gpu()]

    def __reduce__(self) -> Any:
        """Make the class pickleable by serializing the Rust object to a string."""
        # Serialize the Rust object to a string
        serialized = self._r.serialize()
        # Return a tuple: (callable, args) where callable reconstructs the object
        return (self._reconstruct, (serialized,))

    @classmethod
    def _reconstruct(cls, serialized: str) -> WorkerGroup:
        """Reconstruct a Worker from a serialized string."""
        # Deserialize the string back to a Rust Worker
        rust_worker = rust.WorkerGroup.deserialize(serialized)
        # Create a new Python WorkerGroup instance
        return cls(rust_worker)

    def __hash__(self) -> int:
        return hash(self._r.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WorkerGroup):
            return False
        return self._r.id == other._r.id

    def __repr__(self) -> str:
        return self._r.__repr__()

    def __str__(self) -> str:
        return self._r.__str__()