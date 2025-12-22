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
    window_size_left, window_size_right = window_size
    
    q_start = q_range.start
    q_end = q_range.end
    k_start = k_range.start
    k_end = k_range.end
    
    q_ranges = []
    k_ranges = []
    mask_types = []
    
    # Process each query position
    for q_pos in range(q_start, q_end):
        # Calculate the valid key range for this query position based on sliding window
        k_window_start = q_pos - window_size_left
        k_window_end = q_pos + window_size_right + 1
        
        # Intersect with the actual k_range
        k_valid_start = max(k_window_start, k_start)
        k_valid_end = min(k_window_end, k_end)
        
        # Only add if there's a valid range
        if k_valid_start < k_valid_end:
            q_ranges.append(AttnRange.from_range([q_pos, q_pos + 1]))
            k_ranges.append(AttnRange.from_range([k_valid_start, k_valid_end]))
            mask_types.append(AttnMaskType.SLIDING_WINDOW)
    
    return q_ranges, k_ranges, mask_types