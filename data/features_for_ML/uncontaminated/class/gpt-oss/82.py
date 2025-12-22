from __future__ import annotations

import pickle
from typing import Any, List

# Assume these imports are available in the environment
import rust
from rust import WorkerResourcesInternal


class WorkerGroup:
    """
    A lightweight Python wrapper around the Rust `WorkerGroup` type.
    """

    @classmethod
    def make(cls, id: str, stage_name: str, allocations: List[WorkerResourcesInternal]) -> "WorkerGroup":
        """
        Construct a new :class:`WorkerGroup` from the given parameters.
        """
        rust_worker = rust.WorkerGroup(id, stage_name, allocations)
        return cls(rust_worker)

    def __init__(self, rust_worker: rust.WorkerGroup):
        """
        Initialise the wrapper with an existing Rust `WorkerGroup` instance.
        """
        self._rust = rust_worker

    @property
    def id(self) -> str:
        return self._rust.id

    @property
    def stage_name(self) -> str:
        return self._rust.stage_name

    @property
    def allocations(self) -> List[WorkerResourcesInternal]:
        return list(self._rust.allocations)

    @property
    def rust(self) -> rust.WorkerGroup:
        return self._rust

    def split_allocation_per_gpu(self) -> List[WorkerResourcesInternal]:
        """
        Return the allocation list split per GPU.  The default implementation
        simply returns the original allocation list; subclasses may override
        this behaviour.
        """
        return list(self._rust.allocations)

    def __reduce__(self) -> Any:
        """
        Support pickling by serialising the underlying Rust object.
        """
        # Use pickle to serialise the Rust object; this works if the Rust type
        # implements the `pickle` protocol.  If not, fall back to repr.
        try:
            data = pickle.dumps(self._rust)
            return (self._reconstruct, (data,))
        except Exception:
            # Fallback: use repr
            return (self._reconstruct, (repr(self._rust),))

    @classmethod
    def _reconstruct(cls, serialized: Any) -> "WorkerGroup":
        """
        Reconstruct a :class:`WorkerGroup` from the pickled data.
        """
        if isinstance(serialized, bytes):
            rust_worker = pickle.loads(serialized)
        else:
            # Assume string representation
            rust_worker = eval(serialized, {"rust": rust, "WorkerResourcesInternal": WorkerResourcesInternal})
        return cls(rust_worker)

    def __hash__(self) -> int:
        return hash((self.id, self.stage_name, tuple(self.allocations)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WorkerGroup):
            return NotImplemented
        return (
            self.id == other.id
            and self.stage_name == other.stage_name
            and self.allocations == other.allocations
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id!r}, "
            f"stage_name={self.stage_name!r}, "
            f"allocations={self.allocations!r})"
        )

    def __str__(self) -> str:
        return f"WorkerGroup(id={self.id}, stage={self.stage_name}, allocations={len(self.allocations)})"