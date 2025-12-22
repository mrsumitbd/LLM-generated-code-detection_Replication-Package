import numpy as np

_TEMPORAL_ALIGN = 16
_SPATIAL_ALIGN = 32

def pad_video_batch(
    batch: np.ndarray,
    temporal_align: int = _TEMPORAL_ALIGN,
    spatial_align: int = _SPATIAL_ALIGN,
) -> tuple[np.ndarray, list[int]]:
    batch_shape = batch.shape
    pad_temporal = temporal_align - (batch_shape[1] % temporal_align)
    pad_spatial = spatial_align - (batch_shape[2] % spatial_align)
    
    pad_width = ((0, 0), (0, pad_temporal), (0, pad_spatial), (0, pad_spatial), (0, 0))
    padded_batch = np.pad(batch, pad_width, mode='reflect')
    
    crop_region = [0, batch_shape[1], 0, batch_shape[2]]
    
    return padded_batch, crop_region