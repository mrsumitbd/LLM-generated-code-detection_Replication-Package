import numpy as np
import torch
import torch.nn.functional as F
from .triton_ops import dtw_kernel

def dtw_cuda(x, BLOCK_SIZE=1024):
    from .triton_ops import dtw_kernel

    M, N = x.shape
    assert M < BLOCK_SIZE, f"M should be smaller than {BLOCK_SIZE=}"

    x_skew = (
        F.pad(x, (0, M + 1), value=np.inf).flatten()[: M * (N + M)].reshape(M, N + M)
    )
    x_skew = x_skew.T.contiguous()
    cost = torch.ones(N + M + 2, M + 2) * np.inf
    cost[0, 0] = 0
    cost = cost.cuda()
    trace = torch.zeros_like(cost, dtype=torch.int32)

    dtw_kernel[(1,)](
        cost,
        trace,
        x_skew,
        x_skew.stride(0),
        cost.stride(0),
        trace.stride(0),
        N,
        M,
        BLOCK_SIZE=BLOCK_SIZE,
    )

    trace = trace.T.flatten()[: (M + 1) * (M + N + 3)].reshape(M + 1, M + N + 3)[
        :, : N + 1
    ]
    return backtrace(trace.cpu().numpy())