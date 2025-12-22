def infer_attn_mask_from_sliding_window(
    q_range: AttnRange,
    k_range: AttnRange,
    window_size: tuple[int, int],
) -> tuple[AttnRanges, AttnRanges, list[AttnMaskType]]:
    q_ranges = []
    k_ranges = []
    attn_mask_types = []

    q_start, q_end = q_range.start, q_range.end
    k_start, k_end = k_range.start, k_range.end
    window_left, window_right = window_size

    for q in range(q_start, q_end, window_left):
        for k in range(k_start, k_end, window_right):
            q_ranges.append(AttnRange.from_range([q, min(q + window_left, q_end)]))
            k_ranges.append(AttnRange.from_range([k, min(k + window_right, k_end)]))
            attn_mask_types.append(AttnMaskType.SLIDING_WINDOW)

    return q_ranges, k_ranges, attn_mask_types