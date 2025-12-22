import math
from typing import Tuple

def choose_ref_block(
    block_size: Tuple[int, int], swap_ab: bool = False
) -> Tuple[int, int]:
    """
    Choose the proper reference block size for different Q/K block sizes,
    currently for uniform block mask.

    Rules:
    - ref_q_block_size must be a multiple of 64 and >= q_block_size
    - ref_k_block_size must be a multiple of 16 and >= k_block_size
    """
    q_block, k_block = block_size

    # If swap_ab is True, treat the input as swapped
    if swap_ab:
        q_block, k_block = k_block, q_block

    # Compute the smallest multiples that satisfy the constraints
    ref_q_block_size = math.ceil(q_block / 64) * 64
    ref_k_block_size = math.ceil(k_block / 16) * 16

    return ref_q_block_size, ref_k_block_size