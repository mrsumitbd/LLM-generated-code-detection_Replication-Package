class GpuAllocationInternal:
    def __init__(self, offset: int, used_fraction: float):
        self.offset = offset
        self.used_fraction = used_fraction

    @classmethod
    def from_rust(cls, rust_gpu_allocation: rust.GpuAllocation) -> GpuAllocationInternal:
        return cls(rust_gpu_allocation.offset, rust_gpu_allocation.used_fraction)

    def to_rust(self) -> rust.GpuAllocation:
        return rust.GpuAllocation(self.offset, self.used_fraction)