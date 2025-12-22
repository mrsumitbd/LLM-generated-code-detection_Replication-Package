from magi_attention.common.range import AttnRange
from magi_attention.common.enum import AttnMaskType
from magi_attention.common.ranges import AttnRanges

def infer_attn_mask_from_sliding_window(
    q_range: AttnRange,
    k_range: AttnRange,
    window_size: tuple[int, int],
) -> tuple[AttnRanges, AttnRanges, list[AttnMaskType]]:
    """Convert only one sliding window masks into representations using q_range, k_range, and mask type.
    The mask type is specified using window_size.

    Args:
        q_range (AttnRange): q_range of this sliding window mask
        k_range (AttnRange): k_range of this sliding window mask
        window_size (tuple[int, int]): window_size of sliding window mask
            which represents ``[window_size_left, window_size_right]``

    Returns:
        tuple[AttnRanges, AttnRanges, list[AttnMaskType]]:
            processed ``(q_ranges, k_ranges, masktypes)`` triple, sliding window mask have been cutted
            into triple representation.

    Example:
        Here's an example of ``infer_attn_mask_from_sliding_window``::

            >>> q_ranges, k_ranges, attn_mask_type = infer_attn_mask_from_sliding_window(
            ...     q_range=AttnRange.from_range([5, 15]),
            ...     k_range=AttnRange.from_range([5, 15]),
            ...     window_size=(2, 3),
            ... )

        The code above represents the sliding window mask within the ``[5, 15] x [5, 15]`` region
        with a window size of ``(2, 3)``.
    """
    assert len(window_size) == 2, "window size must be of 2 int"

    q_ranges_, k_ranges_ = AttnRanges(), AttnRanges()
    attn_mask_type_: list[AttnMaskType] = []

    # remove the invalid parts in q_range
    q_range_global = q_range
    if q_range.seqlen > k_range.seqlen:
        q_range_global = AttnRange(
            start=q_range.end - k_range.seqlen,
            end=q_range.end,
        )

    # When window_size is -1 or k_range.seqlen - 1, we increment it to avoid splitting the full mask in the result.
    left_window_size = (
        window_size[0]
        if window_size[0] != -1 and window_size[0] < k_range.seqlen - 1
        else k_range.seqlen
    )
    right_window_size = (
        window_size[1]
        if window_size[1] != -1 and window_size[1] < k_range.seqlen - 1
        else k_range.seqlen
    )
    # The principle of the algorithm is to first expand the sliding window mask into a bi-causal one,
    # and then use the slicing algorithm in the slice maker to cut the bi-causal mask to get the sliced sliding window mask.
    # And precisely because we are only simulating the expansion of the bi-causal mask,
    # the left and right window_size can exceed k_range.seqlen - 1 at this point. Compute the expanded bi-causal k_range here.
    slice_k_range_start = k_range.end - q_range_global.seqlen - left_window_size
    slice_k_range_end = k_range.end + right_window_size

    # Compute the region of the k_range that actually needs to be calculated.
    k_range_global = AttnRange(
        start=max(k_range.start, slice_k_range_start),
        end=k_range.end,
    )

    # The following is the logic for slicing the bi-causal mask in the slice maker.
    # First, define the variables needed for the slicing process.
    causal_start = slice_k_range_end - q_range_global.seqlen
    diff_len_of_k_range_minus_q_range = max(
        0,
        slice_k_range_end - slice_k_range_start - q_range_global.seqlen,
    )

    # calculate k_range exceed slice_start, the maxValue not exceed slice_q_range.seqlen
    range_start_exceed_slice_start = min(
        k_range_global.start - slice_k_range_start,
        q_range_global.seqlen,
    )
    range_end_exceed_slice_start = min(
        k_range_global.end - slice_k_range_start,
        q_range_global.seqlen,
    )

    # calculate k_range exceed causal start, the minValue not less than 0
    range_end_exceed_causal_start = max(0, k_range_global.end - causal_start)
    range_start_exceed_causal_start = max(0, k_range_global.start - causal_start)

    # Draw vertical lines from the two endpoints of k_range,
    # which intersect the two hypotenuses of the bi-causal mask at two points.
    # Calculate the vertical coordinates (heights) of these two intersection points,
    # and determine which point is above the other by comparison.
    short_length = min(range_start_exceed_slice_start, range_end_exceed_causal_start)
    long_length = max(range_start_exceed_slice_start, range_end_exceed_causal_start)

    # (part1) calculate q_range and k_range of causal slice
    causal_q_range_local = AttnRange(
        start=q_range_global.start + range_start_exceed_causal_start,
        end=q_range_global.start + short_length,
    )
    causal_k_range_local = AttnRange(
        start=k_range_global.start,
        end=min(
            k_range_global.end,
            k_range_global.start + diff_len_of_k_range_minus_q_range,
        ),
    )

    # (part2) calculate q_range of full or bi_causal slice
    full_or_bi_causal_q_range_local = AttnRange(
        start=q_range_global.start + short_length,
        end=q_range_global.start + long_length,
    )

    # (part3) calculate q_range and k_range of inv_causal slice
    inv_causal_q_range_local = AttnRange(
        start=q_range_global.start + long_length,
        end=q_range_global.start + range_end_exceed_slice_start,
    )
    inv_causal_k_range_local = AttnRange(
        start=max(
            k_range_global.start,
            k_range_global.end - diff_len_of_k_range_minus_q_range,
        ),
        end=k_range_global.end,
    )

    # exclude invalid causal slice
    if causal_q_range_local.seqlen > 0:
        q_ranges_.append(causal_q_range_local)
        k_ranges_.append(causal_k_range_local)
        attn_mask_type_.append(AttnMaskType.CAUSAL)

    # exclude invalid full or bi_causal slice
    if full_or_bi_causal_q_range_local.seqlen > 0:
        q_ranges_.append(full_or_bi_causal_q_range_local)
        k_ranges_.append(k_range_global)
        attn_mask_type_.append(
            AttnMaskType.FULL
            if range_start_exceed_slice_start > range_end_exceed_causal_start
            else AttnMaskType.BICAUSAL
        )

    # exclude invalid inv_causal slice
    if inv_causal_q_range_local.seqlen > 0:
        q_ranges_.append(inv_causal_q_range_local)
        k_ranges_.append(inv_causal_k_range_local)
        attn_mask_type_.append(AttnMaskType.INVCAUSAL)

    return q_ranges_, k_ranges_, attn_mask_type_