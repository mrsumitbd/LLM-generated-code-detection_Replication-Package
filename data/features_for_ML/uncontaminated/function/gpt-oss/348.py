from typing import Tuple, List

# Assume these types are defined elsewhere in the codebase.
# They are imported here for type checking purposes.
try:
    from .types import AttnRange, AttnRanges, AttnMaskType
except Exception:
    # Fallback definitions for type checking only.
    class AttnRange:
        def __init__(self, start: int, end: int):
            self.start = start
            self.end = end

        @classmethod
        def from_range(cls, rng: List[int]):
            return cls(rng[0], rng[1])

    AttnRanges = List[AttnRange]

    class AttnMaskType:
        SLIDING_WINDOW = "sliding_window"


def infer_attn_mask_from_sliding_window(
    q_range: AttnRange,
    k_range: AttnRange,
    window_size: Tuple[int, int],
) -> Tuple[AttnRanges, AttnRanges, List[AttnMaskType]]:
    """
    Convert a sliding window mask into a list of (q_range, k_range, mask_type) triples.

    The sliding window mask is defined by a query range `q_range`, a key range `k_range`,
    and a window size `(left, right)`. For each query position `q` in `q_range`,
    the allowed key positions are `[q - left, q + right]` clipped to `k_range`.

    The function groups consecutive query positions that share the same key range
    into a single segment. Each segment is represented by an `AttnRange` for the
    query positions, an `AttnRange` for the key positions, and the mask type
    `AttnMaskType.SLIDING_WINDOW`.

    Args:
        q_range (AttnRange): The query range of the sliding window mask.
        k_range (AttnRange): The key range of the sliding window mask.
        window_size (tuple[int, int]): The left and right window sizes.

    Returns:
        tuple[AttnRanges, AttnRanges, list[AttnMaskType]]:
            A tuple containing:
            - A list of query ranges (`AttnRanges`).
            - A list of key ranges (`AttnRanges`).
            - A list of mask types (`list[AttnMaskType]`).
    """
    q_start, q_end = q_range.start, q_range.end
    k_start, k_end = k_range.start, k_range.end
    left, right = window_size

    q_ranges: AttnRanges = []
    k_ranges: AttnRanges = []
    masktypes: List[AttnMaskType] = []

    # Initialize the first segment
    cur_q_start = q_start
    cur_k_start = max(k_start, q_start - left)
    cur_k_end = min(k_end, q_start + right)

    for q in range(q_start + 1, q_end + 1):
        k_s = max(k_start, q - left)
        k_e = min(k_end, q + right)

        # If the key range changes, close the current segment
        if k_s != cur_k_start or k_e != cur_k_end:
            # Append the current segment
            q_ranges.append(AttnRange(cur_q_start, q - 1))
            k_ranges.append(AttnRange(cur_k_start, cur_k_end))
            masktypes.append(AttnMaskType.SLIDING_WINDOW)

            # Start a new segment
            cur_q_start = q
            cur_k_start = k_s
            cur_k_end = k_e

    # Append the final segment
    q_ranges.append(AttnRange(cur_q_start, q_end))
    k_ranges.append(AttnRange(cur_k_start, cur_k_end))
    masktypes.append(AttnMaskType.SLIDING_WINDOW)

    return q_ranges, k_ranges, masktypes