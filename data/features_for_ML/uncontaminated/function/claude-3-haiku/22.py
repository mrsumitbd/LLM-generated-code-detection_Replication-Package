def choose_ref_block(
    block_size: tuple[int, int], swap_ab: bool = False
) -> tuple[int, int]:
    q_block_size, k_block_size = block_size if not swap_ab else (k_block_size, q_block_size)

    ref_q_block_size = (q_block_size + 63) // 64 * 64
    ref_k_block_size = (k_block_size + 15) // 16 * 16

    return (ref_q_block_size, ref_k_block_size) if not swap_ab else (ref_k_block_size, ref_q_block_size)