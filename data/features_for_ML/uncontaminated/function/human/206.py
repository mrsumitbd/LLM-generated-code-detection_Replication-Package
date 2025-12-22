import torch
import triton

def ring_reduce_after_scatter(
    rank,
    num_ranks,
    scatter_out,  # [M, N]
    stream,
):
    M, N = scatter_out.shape
    M_per_rank = M // num_ranks
    output = torch.empty((M_per_rank, N), dtype=scatter_out.dtype, device=scatter_out.device)
    grid = lambda META: (triton.cdiv(M_per_rank * N, META["BLOCK_SIZE"]), )
    with torch.cuda.stream(stream):
        kernel_consumer_reduce[grid](
            scatter_out,
            output,
            M_per_rank,
            N,
            rank=rank,
            num_ranks=num_ranks,
            BLOCK_SIZE=2048,
            num_warps=2,
        )

    return output