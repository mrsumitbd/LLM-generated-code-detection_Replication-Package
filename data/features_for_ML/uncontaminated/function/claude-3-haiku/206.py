import torch

def ring_reduce_after_scatter(
    rank,
    num_ranks,
    scatter_out,  # [M, N]
    stream,
):
    device = scatter_out.device
    dtype = scatter_out.dtype
    M, N = scatter_out.shape

    # Allocate buffers
    recv_buffer = torch.empty((M, N), device=device, dtype=dtype)
    send_buffer = torch.empty((M, N), device=device, dtype=dtype)

    # Perform ring reduction
    send_buffer.copy_(scatter_out)
    for i in range(1, num_ranks):
        src = (rank - i) % num_ranks
        dst = (rank + 1) % num_ranks
        with torch.cuda.stream(stream):
            torch.distributed.recv(recv_buffer, src=src)
            torch.distributed.send(send_buffer, dst=dst)
            scatter_out.add_(recv_buffer)
        send_buffer.copy_(scatter_out)

    return scatter_out