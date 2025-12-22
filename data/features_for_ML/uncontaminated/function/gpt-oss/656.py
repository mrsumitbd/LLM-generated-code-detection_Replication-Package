from dataclasses import dataclass
from typing import Any

@dataclass
class ReduceScatter2DContext:
    max_M: int
    N: int
    rank: int
    world_size: int
    local_world_size: int
    dtype: Any
    overlap_with_gemm: bool
    num_reduction_sms: int
    local_rank: int
    node_rank: int
    num_nodes: int

def create_reduce_scater_2d_ctx(
    max_M,
    N,
    rank,
    world_size,
    local_world_size,
    dtype,
    overlap_with_gemm=True,
    num_reduction_sms=15,
) -> ReduceScatter2DContext:
    """
    Create a ReduceScatter2DContext for a 2‑D reduce‑scatter operation.

    Parameters
    ----------
    max_M : int
        Maximum number of rows in the local matrix.
    N : int
        Number of columns in the local matrix.
    rank : int
        Global rank of the current process.
    world_size : int
        Total number of processes in the communicator.
    local_world_size : int
        Number of processes on the same node.
    dtype : Any
        Data type of the tensors.
    overlap_with_gemm : bool, optional
        Whether to overlap the local reduction with GEMM.
    num_reduction_sms : int, optional
        Number of SMs to use for the reduction kernel.

    Returns
    -------
    ReduceScatter2DContext
        Context object containing all relevant information for the operation.
    """
    # Compute local and node ranks
    local_rank = rank % local_world_size
    node_rank = rank // local_world_size
    num_nodes = world_size // local_world_size

    # Clamp the number of reduction SMs to a reasonable range
    # (e.g., not exceeding the total number of SMs on the device)
    try:
        import torch
        device = torch.cuda.current_device()
        total_sms = torch.cuda.get_device_properties(device).multi_processor_count
        num_reduction_sms = min(num_reduction_sms, total_sms)
    except Exception:
        # If torch is not available or device info cannot be retrieved,
        # keep the provided value.
        pass

    return ReduceScatter2DContext(
        max_M=max_M,
        N=N,
        rank=rank,
        world_size=world_size,
        local_world_size=local_world_size,
        dtype=dtype,
        overlap_with_gemm=overlap_with_gemm,
        num_reduction_sms=num_reduction_sms,
        local_rank=local_rank,
        node_rank=node_rank,
        num_nodes=num_nodes,
    )