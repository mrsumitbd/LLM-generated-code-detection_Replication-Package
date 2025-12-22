import triton.language as tl
from triton_dist.language.extra import libshmem_device
from triton.language.extra.cuda.language_extra import (
    __syncthreads,
    pack_b32_v2,
    tid,
    ntid,
    load_v4_u32,
    load_v2_b64,
    st_v2_u32,
    st,
    multimem_st_b64,
)

def _recv_ll_and_multimem_st_block(dest_ptr, src_ptr, num_ints, ll_flag):
    """split src/dest outside of _recv_ll. this function is designed for a threadblock

    num_ints: of the pre-LL-packed num_ints.
    """
    thread_idx = tid(0)
    block_size = ntid(0)
    src_ptr = tl.cast(src_ptr, tl.pointer_type(tl.int32))
    dest_ptr = tl.cast(dest_ptr, tl.pointer_type(tl.int32))
    dest_mc_ptr = libshmem_device.remote_mc_ptr(libshmem_device.NVSHMEMX_TEAM_NODE, dest_ptr)
    # manual load per vec
    for n in range(thread_idx, num_ints // 2, block_size):
        data1, flag1, data2, flag2 = load_v4_u32(src_ptr + n * 4)
        while flag1 != ll_flag or flag2 != ll_flag:
            data1, flag1, data2, flag2 = load_v4_u32(src_ptr + n * 4)
        multimem_st_b64(dest_mc_ptr + n * 2, pack_b32_v2(data1, data2))