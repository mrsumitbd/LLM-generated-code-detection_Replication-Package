import torch
import torch.distributed as dist

def ring_reduce_after_scatter(
    rank,
    num_ranks,
    scatter_out,  # [M, N]
    stream,
):
    """
    Perform a ring‑style reduction (sum) on the local chunk `scatter_out`.
    The result is written back into `scatter_out` in place.

    Parameters
    ----------
    rank : int
        Rank of the current process (unused, kept for API compatibility).
    num_ranks : int
        Total number of ranks (unused, kept for API compatibility).
    scatter_out : torch.Tensor
        Local chunk of data to be reduced.  It will be modified in place.
    stream : torch.cuda.Stream or None
        CUDA stream to use for the operation.  If None, the default stream
        is used.
    """
    # Ensure we are in the correct CUDA stream if provided
    if stream is not None:
        with torch.cuda.stream(stream):
            dist.all_reduce(scatter_out, op=dist.ReduceOp.SUM)
    else:
        dist.all_reduce(scatter_out, op=dist.ReduceOp.SUM)