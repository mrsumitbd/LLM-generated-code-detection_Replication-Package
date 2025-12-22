import numpy as np
from scipy.signal import resample

def audio_resample(data, config: DataConfig):
    """Resample data.
       Inplace operation.
    """
    original_length = data.shape[-1]
    new_length = int(original_length * config.sample_rate_ratio)
    data[:] = resample(data, new_length, axis=-1)