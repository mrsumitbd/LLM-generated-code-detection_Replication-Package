def _recv_ll_and_multimem_st_block(dest_ptr, src_ptr, num_ints, ll_flag):
    """split src/dest outside of _recv_ll. this function is designed for a threadblock

    num_ints: of the pre-LL-packed num_ints.
    """
    import numpy as np

    if ll_flag:
        # Receive the long-latency data
        ll_data = np.frombuffer(memoryview(src_ptr.to_bytes(num_ints * 4, byteorder='little')), dtype=np.int32)
        # Store the long-latency data
        dest_ptr[:] = ll_data
    else:
        # Receive the short-latency data
        sl_data = np.frombuffer(memoryview(src_ptr.to_bytes(num_ints * 4, byteorder='little')), dtype=np.int32)
        # Store the short-latency data
        dest_ptr[:] = sl_data