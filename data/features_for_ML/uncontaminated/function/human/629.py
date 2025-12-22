import numpy as np

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
    num_frames, height, width = batch.shape[-4:-1]
    align = spatial_align
    height_to_pad = (align - height % align) if height % align != 0 else 0
    width_to_pad = (align - width % align) if width % align != 0 else 0

    align = temporal_align
    frames_to_pad = (align - (num_frames - 1) % align) if (num_frames - 1) % align != 0 else 0

    crop_region = [
        frames_to_pad >> 1,
        height_to_pad >> 1,
        width_to_pad >> 1,
        num_frames + (frames_to_pad >> 1),
        height + (height_to_pad >> 1),
        width + (width_to_pad >> 1),
    ]
    batch = np.pad(
        batch,
        (
            (0, 0),
            (0, 0),
            (height_to_pad >> 1, height_to_pad - (height_to_pad >> 1)),
            (width_to_pad >> 1, width_to_pad - (width_to_pad >> 1)),
            (0, 0),
        ),
        mode="constant",
    )
    batch = np.pad(
        batch,
        (
            (0, 0),
            (frames_to_pad >> 1, frames_to_pad - (frames_to_pad >> 1)),
            (0, 0),
            (0, 0),
            (0, 0),
        ),
        mode="edge",
    )
    return batch, crop_region