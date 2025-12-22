import numpy as np
import math

# Default alignment values (should be defined elsewhere in the module)
# If not defined, fall back to 1 to avoid errors.
try:
    _TEMPORAL_ALIGN
except NameError:
    _TEMPORAL_ALIGN = 1
try:
    _SPATIAL_ALIGN
except NameError:
    _SPATIAL_ALIGN = 1

def pad_video_batch(
    batch: np.ndarray,
    temporal_align: int = _TEMPORAL_ALIGN,
    spatial_align: int = _SPATIAL_ALIGN,
) -> tuple[np.ndarray, list[int]]:
    """
    Pads a batch of videos to be divisible by `temporal_align` or `spatial_align`.

    Zero pad spatially. Reflection pad temporally to handle causality better.

    Args:
        batch: The batch of videos to pad, layout BxFxHxWx3, in any range.
        temporal_align: The alignment to pad the temporal dimension to.
        spatial_align: The alignment to pad the spatial dimensions to.

    Returns:
        The padded batch and the crop region.
        The crop region is a list of six integers:
        [temporal_start, temporal_end, height_start, height_end, width_start, width_end]
        which can be used to crop the padded batch back to the original size.
    """
    if batch.ndim != 5:
        raise ValueError(f"Expected batch of shape (B, F, H, W, 3), got {batch.shape}")

    B, F, H, W, C = batch.shape

    # Compute new sizes
    new_F = math.ceil(F / temporal_align) * temporal_align
    new_H = math.ceil(H / spatial_align) * spatial_align
    new_W = math.ceil(W / spatial_align) * spatial_align

    # Pad amounts
    pad_F = new_F - F
    pad_H = new_H - H
    pad_W = new_W - W

    pad_before_F = pad_F // 2
    pad_after_F = pad_F - pad_before_F

    pad_before_H = pad_H // 2
    pad_after_H = pad_H - pad_before_H

    pad_before_W = pad_W // 2
    pad_after_W = pad_W - pad_before_W

    # Pad widths for each axis
    pad_width = (
        (0, 0),  # batch
        (pad_before_F, pad_after_F),  # temporal
        (pad_before_H, pad_after_H),  # height
        (pad_before_W, pad_after_W),  # width
        (0, 0),  # channels
    )

    # Modes per axis: constant for batch, reflect for temporal, constant for spatial, constant for channels
    modes = ("constant", "reflect", "constant", "constant", "constant")

    padded = np.pad(batch, pad_width, mode=modes, constant_values=0)

    # Crop region to recover original video
    crop_region = [
        pad_before_F,
        pad_before_F + F,
        pad_before_H,
        pad_before_H + H,
        pad_before_W,
        pad_before_W + W,
    ]

    return padded, crop_region