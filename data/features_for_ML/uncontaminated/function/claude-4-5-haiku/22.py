def choose_ref_block(
    block_size: tuple[int, int], swap_ab: bool = False
) -> tuple[int, int]:
    """
    Choose the proper reference block size for different Q/K block sizes, currently for uniform block mask.

    Rules:
    - ref_q_block_size must be a multiple of 64 and >= q_block_size
    - ref_k_block_size must be a multiple of 16 and >= k_block_size
    """
    q_block_size, k_block_size = block_size
    
    # Find the smallest multiple of 64 that is >= q_block_size
    ref_q_block_size = ((q_block_size + 63) // 64) * 64
    
    # Find the smallest multiple of 16 that is >= k_block_size
    ref_k_block_size = ((k_block_size + 15) // 16) * 16
    
    if swap_ab:
        return (ref_k_block_size, ref_q_block_size)
    else:
        return (ref_q_block_size, ref_k_block_size)