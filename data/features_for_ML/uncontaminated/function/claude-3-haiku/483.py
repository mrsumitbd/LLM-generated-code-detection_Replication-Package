import torch
import triton
import triton.language as tl

@triton.jit
def chunk_kkt_inv_ut_fused_kernel(
    k,
    v,
    beta,
    g,
    cu_seqlens,
    chunk_indices,
    A,
    g_cumsum,
    Ai,
    w,
    u,
    T,
    NT,
    H: tl.constexpr,
    K: tl.constexpr,
    V: tl.constexpr,
    BT: tl.constexpr,
    BK: tl.constexpr,
    BV: tl.constexpr,
    USE_G: tl.constexpr = True,
):
    # Get the block and thread IDs
    pid = tl.program_id(axis=0)
    block_start = pid * BT
    block_end = min(block_start + BT, T)

    # Initialize the output buffers
    g_cumsum[block_start:block_end] = 0
    Ai[block_start:block_end] = 0
    w[block_start:block_end] = 0
    u[block_start:block_end] = 0

    # Compute the chunk indices
    chunk_start = chunk_indices[block_start]
    chunk_end = chunk_indices[block_end]

    # Compute the cumulative sum of g
    if USE_G:
        for t in range(block_start, block_end):
            for h in range(H):
                g_cumsum[t, h] = tl.load(g, (t, h))
                if t > block_start:
                    g_cumsum[t, h] += g_cumsum[t - 1, h]

    # Compute the KKT inverse and U^T
    for t in range(block_start, block_end):
        for h in range(H):
            for i in range(BT):
                idx = chunk_start + i
                Ai[t, h, i] = tl.load(k, (idx, h))
                A[t, h, i] = Ai[t, h, i]

    tl.barrier()

    for t in range(block_start, block_end):
        for h in range(H):
            for i in range(BT):
                idx = chunk_start + i
                for j in range(BT):
                    Ai[t, h, i] -= tl.load(A, (t, h, j)) * tl.load(A, (t, h, j, i))
            for i in range(BT):
                idx = chunk_start + i
                w[t, h, i] = tl.load(v, (idx, h))
                for j in range(BT):
                    w[t, h, i] -= tl.load(A, (t, h, j, i)) * tl.load(w, (t, h, j))
            for i in range(BV):
                idx = chunk_start + i
                u[t, h, i] = tl.load(v, (idx + BT * H, h))
                for j in range(BT):
                    u[t, h, i] -= tl.load(A, (t, h, j, i + BT * H)) * tl.load(w, (t, h, j))

    # Apply the scaling factor
    for t in range(block_start, block_end):
        for h in range(H):
            for i in range(BT):
                Ai[t, h, i] *= beta
            for i in range(BK):
                w[t, h, i] *= beta
            for i in range(BV):
                u[t, h, i] *= beta