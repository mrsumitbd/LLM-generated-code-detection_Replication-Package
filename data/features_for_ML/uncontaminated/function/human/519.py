import triton.language as tl
import triton_dist.language as tdl
from triton.language.extra.cuda.language_extra import tid, __syncthreads, st

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
    tl.static_assert(BLOCK_SIZE_N % head_dim == 0, "BLOCK_SIZE_N must be divisible by head_dim")
    num_heads_per_gemm_tile: tl.constexpr = BLOCK_SIZE_N // head_dim

    for i in tl.static_range(sp_size + 1):
        tl.store(cum_seqlen_gpu_ptr + i, cum_seqlen_cpu_tuple[i])
    __syncthreads()

    if NUM_COMM_SMS >= sp_size:
        tl.static_assert(NUM_COMM_SMS % sp_size == 0, "NUM_COMM_SMS must be divisible by sp_size")
        SMS_per_sp_rank: tl.constexpr = NUM_COMM_SMS // sp_size
        SP_rank_per_sm: tl.constexpr = 1
    else:
        tl.static_assert(sp_size % NUM_COMM_SMS == 0, "sp_size must be divisible by NUM_COMM_SMS")
        SMS_per_sp_rank: tl.constexpr = 1
        SP_rank_per_sm = sp_size // NUM_COMM_SMS

    pid = tl.program_id(axis=0)
    rank_offset = rank - sp_rank

    for tile in range(SP_rank_per_sm):
        remote_sp_rank = pid * SP_rank_per_sm // SMS_per_sp_rank + tile
        remote_rank = rank_offset + remote_sp_rank

        remote_gemm_out_ptr = tdl.symm_at(gemm_out_ptr, remote_rank)
        if NEED_BARRIER:
            remote_gemm_barrier_ptr = tdl.symm_at(gemm_barrier_ptr, remote_rank)

        seq_len_beg = tl.load(cum_seqlen_gpu_ptr + remote_sp_rank)
        seq_len_end = tl.load(cum_seqlen_gpu_ptr + remote_sp_rank + 1)
        seq_len = seq_len_end - seq_len_beg
        num_tiles_m = tl.cdiv(seq_len, BLOCK_SIZE_M)
        tl.static_assert(qkv_out_features % head_dim == 0, "qkv_out_features must be divisible by head_dim")
        num_tiles_n: tl.constexpr = qkv_out_features // head_dim  # number of heads in total
        tl.static_assert(num_tiles_n % sp_size == 0, "num_tiles_n must be divisible by sp_size")
        num_tiles_n_per_sp_rank: tl.constexpr = num_tiles_n // sp_size
        num_tiles_n_for_q: tl.constexpr = num_tiles_n // (gqa + 2 * HAS_KV) * gqa
        num_tiles_n_for_k: tl.constexpr = num_tiles_n // (gqa + 2 * HAS_KV) * HAS_KV
        num_tiles_n_per_sp_rank_for_q: tl.constexpr = num_tiles_n_per_sp_rank // (gqa + 2 * HAS_KV) * gqa
        num_tiles_n_per_sp_rank_for_k: tl.constexpr = num_tiles_n_per_sp_rank // (gqa + 2 * HAS_KV) * HAS_KV

        tl.static_assert(qkv_out_features % BLOCK_SIZE_N == 0, "qkv_out_features must be divisible by BLOCK_SIZE_N")
        num_tiles_gemm_n: tl.constexpr = qkv_out_features // BLOCK_SIZE_N
        num_tiles = num_tiles_m * num_tiles_n_per_sp_rank

        offs_m = tl.arange(0, BLOCK_SIZE_M)
        offs_n = tl.arange(0, head_dim)

        for tile_id in range(pid % SMS_per_sp_rank, num_tiles, SMS_per_sp_rank):
            tile_id_m = tile_id // num_tiles_n_per_sp_rank
            tile_id_n = tile_id % num_tiles_n_per_sp_rank

            a2a_out_ptr = q_out_ptr
            a2a_head_id = 0
            gemm_head_id = 0
            a2a_num_head_per_sp_rank = 0

            if tile_id_n < num_tiles_n_per_sp_rank_for_q:
                a2a_out_ptr = q_out_ptr
                a2a_head_id = tile_id_n
                gemm_head_id = a2a_head_id + sp_rank * num_tiles_n_per_sp_rank_for_q
                a2a_num_head_per_sp_rank = num_tiles_n_per_sp_rank_for_q
            elif tile_id_n < num_tiles_n_per_sp_rank_for_q + num_tiles_n_per_sp_rank_for_k:
                if HAS_KV:
                    a2a_out_ptr = k_out_ptr
                    a2a_head_id = tile_id_n - num_tiles_n_per_sp_rank_for_q
                    gemm_head_id = a2a_head_id + num_tiles_n_for_q + sp_rank * num_tiles_n_per_sp_rank_for_k
                    a2a_num_head_per_sp_rank = num_tiles_n_per_sp_rank_for_k
            else:
                if HAS_KV:
                    a2a_out_ptr = v_out_ptr
                    a2a_head_id = tile_id_n - num_tiles_n_per_sp_rank_for_q - num_tiles_n_per_sp_rank_for_k
                    gemm_head_id = a2a_head_id + num_tiles_n_for_q + num_tiles_n_for_k + sp_rank * num_tiles_n_per_sp_rank_for_k
                    a2a_num_head_per_sp_rank = num_tiles_n_per_sp_rank_for_k

            start_seq = tile_id_m * BLOCK_SIZE_M
            end_seq = min(start_seq + BLOCK_SIZE_M, seq_len)

            gemm_out_ptrs = remote_gemm_out_ptr + (tile_id_m * BLOCK_SIZE_M + offs_m[:, None]
                                                   ) * qkv_out_features + gemm_head_id * head_dim + offs_n[None, :]
            gemm_out_mask = (tile_id_m * BLOCK_SIZE_M + offs_m < end_seq)[:, None] & (offs_n < head_dim)[None, :]
            if NEED_BARRIER:
                tile_id_gemm_n = gemm_head_id // num_heads_per_gemm_tile
                barrier_ptr = remote_gemm_barrier_ptr + tile_id_m * num_tiles_gemm_n + tile_id_gemm_n
                token = tdl.wait(barrier_ptr, 1, "sys", "acquire", 1)
                gemm_out_ptrs = tdl.consume_token(gemm_out_ptrs, token)

            data = tl.load(gemm_out_ptrs, mask=gemm_out_mask)

            a2a_offs_m = seq_len_beg + start_seq + offs_m
            a2a_offs_n = a2a_head_id * head_dim + offs_n
            a2a_out_ptrs = a2a_out_ptr + a2a_offs_m[:, None] * a2a_num_head_per_sp_rank * head_dim + a2a_offs_n[None, :]
            a2a_mask = (a2a_offs_m < seq_len_beg + end_seq)[:, None] & (offs_n < head_dim)[None, :]
            tl.store(a2a_out_ptrs, data, mask=a2a_mask)