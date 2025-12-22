class GpuAllocationInternal:
    """Represents the allocation a worker is taking up for a given GPU.

    This class describes how much of a GPU's resources are allocated to a worker.
    It's a lightweight reference that points to a GPU in a node's GPU list rather
    than storing full GPU details.

    Attributes:
        offset: **Index into the node's NodeResources.gpus list**, not the hardware GPU index.
                This indirection allows the same allocation to be used with different nodes,
                and keeps the allocation struct small. To get the actual hardware GPU index
                or UUID, you must look up node_resources.gpus[offset].

        used_fraction: Fraction of the GPU's compute capacity allocated (0.0 to 1.0).
                      For whole-GPU allocations, this is 1.0. For fractional allocations,
                      this can be any value like 0.25, 0.5, etc.

    Important: Offset vs. GPU Index
        The `offset` field is **not** the hardware GPU index! It's the position in the
        NodeResources.gpus list. For example:
        - If a node has 4 GPUs and you want GPU at hardware index 2, you need to find
          which position in the gpus list corresponds to that GPU.
        - The actual hardware index is stored in GpuResources.index
        - The GPU UUID is stored in GpuResources.uuid_

    Example:
        >>> # Create an allocation for the first GPU in a node's list (offset=0)
        >>> # using 50% of its capacity
        >>> alloc = GpuAllocation(offset=0, used_fraction=0.5)
        >>>
        >>> # To get the actual hardware GPU index:
        >>> # hardware_index = node_resources.gpus[alloc.offset].index
    """

    def __init__(self, offset: int, used_fraction: float):
        self.offset = offset
        self.used_fraction = used_fraction

    @classmethod
    def from_rust(cls, rust_gpu_allocation: rust.GpuAllocation) -> GpuAllocationInternal:
        return cls(
            offset=rust_gpu_allocation.offset,
            used_fraction=rust_gpu_allocation.used_fraction,
        )

    def to_rust(self) -> rust.GpuAllocation:
        return rust.GpuAllocation(
            offset=self.offset,
            used_fraction=self.used_fraction,
        )