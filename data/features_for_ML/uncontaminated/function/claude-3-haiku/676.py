import numpy as np
from typing import Any, Callable, Union

@np.vectorize
def amplitude_to_db(
    S: np.ndarray,
    *,
    ref: float | Callable = 1.0,
    amin: float = 1e-5,
    top_db: float | None = 80.0,
) -> np.floating[Any] | np.ndarray:
    """Convert an amplitude spectrogram to dB-scaled spectrogram."""
    if callable(ref):
        ref = ref(S)
    ref = np.maximum(amin, ref)
    S = np.maximum(amin, np.abs(S))
    power = 20 * np.log10(S / ref)
    if top_db is not None:
        power = np.maximum(power, power.max() - top_db)
    return power