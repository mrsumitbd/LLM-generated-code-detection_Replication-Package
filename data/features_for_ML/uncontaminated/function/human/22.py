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
    if swap_ab:
        raise NotImplementedError("SwapAB Attention is not supported yet.")
    else:
        # Tile_M must be a multiple of 64
        if q_block_size >= 64:
            ref_q_block_size = min(192, ((q_block_size + 63) // 64) * 64)
        else:
            ref_q_block_size = 64

        # Tile_K must be a multiple of 16
        if k_block_size >= 16:
            ref_k_block_size = min(256, ((k_block_size + 15) // 16) * 16)
        else:
            ref_k_block_size = 16

        return (ref_q_block_size, ref_k_block_size)