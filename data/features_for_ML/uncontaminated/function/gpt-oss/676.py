import numpy as np
from typing import Any, Callable, Union

def amplitude_to_db(
    S: np.ndarray,
    *,
    ref: Union[float, Callable] = 1.0,
    amin: float = 1e-5,
    top_db: Union[float, None] = 80.0,
) -> np.ndarray:
    """
    Convert an amplitude spectrogram to dB-scaled spectrogram.

    Parameters
    ----------
    S : np.ndarray
        input amplitude

    ref : scalar or callable
        If scalar, the amplitude ``abs(S)`` is scaled relative to ``ref``:
        ``20 * log10(S / ref)``.
        Zeros in the output correspond to positions where ``S == ref``.

        If callable, the reference value is computed as ``ref(S)``.

    amin : float > 0 [scalar]
        minimum threshold for ``S`` and ``ref``

    top_db : float >= 0 [scalar]
        threshold the output at ``top_db`` below the peak:
        ``max(20 * log10(S/ref)) - top_db``

    Returns
    -------
    S_db : np.ndarray
        ``S`` measured in dB
    """
    # Ensure S is a numpy array
    S = np.asarray(S)

    # Compute absolute amplitude and clip to amin
    S_abs = np.abs(S)
    S_abs = np.maximum(S_abs, amin)

    # Compute reference value
    if callable(ref):
        ref_val = ref(S)
        ref_val = np.abs(ref_val)
    else:
        ref_val = np.abs(ref)

    # Clip reference to amin
    ref_val = np.maximum(ref_val, amin)

    # Compute dB
    S_db = 20.0 * np.log10(S_abs / ref_val)

    # Apply top_db clipping if requested
    if top_db is not None:
        max_db = S_db.max()
        S_db = np.maximum(S_db, max_db - top_db)

    return S_db