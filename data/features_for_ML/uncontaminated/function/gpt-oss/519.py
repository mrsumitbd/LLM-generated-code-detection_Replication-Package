import triton
import triton.language as tl

@triton.jit
def kernel_all2all_pull_intra_node_nvl(
    gemm_out_ptr,
    gemm_barrier_ptr,
    cum_seqlen_cpu_tuple,  # sp_size + 1 elems
    cum_seqlen_gpu_ptr,
    q_out_ptr,
    k_out_ptr,
    v_out_ptr,
    sp_size: tl.constexpr,
    rank,
    sp_rank,
    qkv_out_features: tl.constexpr,
    head_dim: tl.constexpr,
    gqa: tl.constexpr,
    BLOCK_SIZE_M: tl.constexpr,
    BLOCK_SIZE_N: tl.constexpr,
    NUM_COMM_SMS: tl.constexpr,
    HAS_KV: tl.constexpr = 1,
    NEED_BARRIER: tl.constexpr = 1,
):
    # This kernel is a placeholder that performs no operations.
    # It is intended to be replaced with the actual intra-node all‑to‑all
    # pull logic when the communication primitives are available.
    return