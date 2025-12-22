def infer_attn_mask_from_sliding_window(q_range: AttnRange, k_range: AttnRange, window_size: tuple[int, int]) -> tuple[AttnRanges, AttnRanges, list[AttnMaskType]]:
    q_ranges = q_range.cut_into_ranges(window_size[0], window_size[1])
    k_ranges = k_range.cut_into_ranges(window_size[0], window_size[1])
    masktypes = [AttnMaskType.SLIDING_WINDOW] * len(q_ranges)
    return q_ranges, k_ranges, masktypes