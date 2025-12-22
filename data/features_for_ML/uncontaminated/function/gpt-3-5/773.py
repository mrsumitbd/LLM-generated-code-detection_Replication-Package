import numpy as np
from typing import Callable

def _signal_to_frame_nonsilent(
    y: np.ndarray,
    frame_length: int = 2048,
    hop_length: int = 512,
    top_db: float = 60,
    ref: Callable | float = np.max,
    aggregate: Callable = np.max,
) -> np.ndarray:
    
    def amplitude_to_db(x):
        return 20 * np.log10(np.maximum(np.abs(x), 1e-10))

    if callable(ref):
        ref_value = ref(np.abs(y))
    else:
        ref_value = ref

    db = amplitude_to_db(y)
    if top_db < 0:
        threshold = ref_value + top_db
    else:
        threshold = ref_value * 10.0 ** (top_db / 20.0)

    if y.ndim > 1:
        axis = tuple(range(y.ndim))[1:]
        non_silent = aggregate(db, axis=axis) > threshold
    else:
        non_silent = db > threshold

    return non_silent