def pad_video_batch(
    batch: np.ndarray,
    temporal_align: int = _TEMPORAL_ALIGN,
    spatial_align: int = _SPATIAL_ALIGN,
) -> tuple[np.ndarray, list[int]]:
    """Pads a batch of videos to be divisible by `temporal_align` or `spatial_align`.

    Zero pad spatially. Reflection pad temporally to handle causality better.
    Args:
        batch: The batch of videos to pad., layout BxFxHxWx3, in any range.
        align: The alignment to pad to.
    Returns:
        The padded batch and the crop region.
    """
    B, F, H, W, C = batch.shape
    
    # Calculate padding needed for temporal dimension
    temporal_pad = (temporal_align - (F % temporal_align)) % temporal_align
    
    # Calculate padding needed for spatial dimensions
    height_pad = (spatial_align - (H % spatial_align)) % spatial_align
    width_pad = (spatial_align - (W % spatial_align)) % spatial_align
    
    # Pad temporally using reflection mode
    if temporal_pad > 0:
        pad_before = temporal_pad // 2
        pad_after = temporal_pad - pad_before
        batch = np.pad(
            batch,
            ((0, 0), (pad_before, pad_after), (0, 0), (0, 0), (0, 0)),
            mode='reflect'
        )
    
    # Pad spatially using constant (zero) mode
    if height_pad > 0 or width_pad > 0:
        pad_top = height_pad // 2
        pad_bottom = height_pad - pad_top
        pad_left = width_pad // 2
        pad_right = width_pad - pad_left
        batch = np.pad(
            batch,
            ((0, 0), (0, 0), (pad_top, pad_bottom), (pad_left, pad_right), (0, 0)),
            mode='constant',
            constant_values=0
        )
    
    # Store crop region as [temporal_start, temporal_end, height_start, height_end, width_start, width_end]
    temporal_start = temporal_pad // 2
    temporal_end = temporal_start + F
    height_start = height_pad // 2
    height_end = height_start + H
    width_start = width_pad // 2
    width_end = width_start + W
    
    crop_region = [temporal_start, temporal_end, height_start, height_end, width_start, width_end]
    
    return batch, crop_region