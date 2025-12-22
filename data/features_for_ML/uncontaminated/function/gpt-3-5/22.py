def choose_ref_block(block_size: tuple[int, int], swap_ab: bool = False) -> tuple[int, int]:
    q_block_size, k_block_size = block_size
    ref_q_block_size = q_block_size if q_block_size % 64 == 0 else (q_block_size // 64 + 1) * 64
    ref_k_block_size = k_block_size if k_block_size % 16 == 0 else (k_block_size // 16 + 1) * 16

    if swap_ab:
        return ref_k_block_size, ref_q_block_size
    else:
        return ref_q_block_size, ref_k_block_size