import numpy as np

def pad_video_batch(
    batch: np.ndarray,
    temporal_align: int = 8,
    spatial_align: int = 32,
) -> tuple[np.ndarray, list[int]]:
    """Pads a batch of videos to be divisible by `temporal_align` or `spatial_align`.

    Zero pad spatially. Reflection pad temporally to handle causality better.
    Args:
        batch: The batch of videos to pad., layout BxFxHxWx3, in any range.
        temporal_align: The temporal alignment to pad to.
        spatial_align: The spatial alignment to pad to.
    Returns:
        The padded batch and the crop region.
    """
    batch_size, num_frames, height, width, _ = batch.shape

    # Temporal padding
    new_num_frames = (num_frames + temporal_align - 1) // temporal_align * temporal_align
    pad_front = (new_num_frames - num_frames) // 2
    pad_back = new_num_frames - num_frames - pad_front
    batch = np.pad(batch, ((0, 0), (pad_front, pad_back), (0, 0), (0, 0), (0, 0)), mode='reflect')

    # Spatial padding
    new_height = (height + spatial_align - 1) // spatial_align * spatial_align
    new_width = (width + spatial_align - 1) // spatial_align * spatial_align
    pad_top = (new_height - height) // 2
    pad_bottom = new_height - height - pad_top
    pad_left = (new_width - width) // 2
    pad_right = new_width - width - pad_left
    batch = np.pad(batch, ((0, 0), (0, 0), (pad_top, pad_bottom), (pad_left, pad_right), (0, 0)), mode='constant', constant_values=0)

    crop_region = [pad_front, pad_back, pad_top, pad_bottom, pad_left, pad_right]
    return batch, crop_region