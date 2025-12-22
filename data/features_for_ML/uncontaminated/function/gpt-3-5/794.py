def _recv_ll_and_multimem_st_block(dest_ptr, src_ptr, num_ints, ll_flag):
    """split src/dest outside of _recv_ll. this function is designed for a threadblock

    num_ints: of the pre-LL-packed num_ints.
    """
    if ll_flag:
        for i in range(num_ints):
            dest_ptr[i] = src_ptr[i]
    else:
        for i in range(num_ints):
            dest_ptr[i] = src_ptr[i * 2] + src_ptr[i * 2 + 1]