import numpy as np

def sequence_mask(length, max_length=None):
    if max_length is None:
        max_length = np.max(length)
    
    mask = np.arange(max_length)[None, :] < np.array(length)[:, None]
    return mask