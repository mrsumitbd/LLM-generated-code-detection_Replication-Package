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
    """Frame-wise non-silent indicator for audio input.

    This is a helper function for `trim` and `split`.

    Parameters
    ----------
    y : np.ndarray
        Audio signal, mono or stereo

    frame_length : int > 0
        The number of samples per frame

    hop_length : int > 0
        The number of samples between frames

    top_db : number
        The threshold (in decibels) below reference to consider as
        silence.
        You can also use a negative value for `top_db` to treat any value
        below `ref + |top_db|` as silent.  This will only make sense if
        `ref` is not `np.max`.

    ref : callable or float
        The reference amplitude

    aggregate : callable [default: np.max]
        Function to aggregate dB measurements across channels (if y.ndim > 1)

        Note: for multiple leading axes, this is performed using ``np.apply_over_axes``.

    Returns
    -------
    non_silent : np.ndarray, shape=(m,), dtype=bool
        Indicator of non-silent frames
    """
    # Ensure y is a numpy array
    y = np.asarray(y)

    # Create frames using sliding_window_view
    # Handle 1D and multi-dimensional signals
    if y.ndim == 1:
        frames = np.lib.stride_tricks.sliding_window_view(y, frame_length)[::hop_length]
    else:
        # Use last axis as time axis
        frames = np.lib.stride_tricks.sliding_window_view(y, frame_length, axis=-1)[::hop_length]
        # frames shape: (..., n_frames, frame_length)

    # Compute RMS per frame
    # For multi-channel, compute RMS per channel first
    if frames.ndim == 2:  # mono
        rms = np.sqrt(np.mean(frames**2, axis=-1))
    else:  # multi-channel
        # frames shape (..., n_frames, frame_length)
        rms = np.sqrt(np.mean(frames**2, axis=-1))
        # rms shape (..., n_frames)

        # Aggregate across leading axes
        # Determine axes to aggregate: all axes except the last (n_frames)
        axes_to_agg = tuple(range(rms.ndim - 1))
        rms = np.apply_over_axes(aggregate, rms, axes=axes_to_agg).reshape(-1)

    # Compute reference value
    if callable(ref):
        ref_val = ref(rms)
    else:
        ref_val = ref

    # Avoid division by zero
    eps = np.finfo(rms.dtype).eps
    rms_safe = np.maximum(rms, eps)

    # Convert to dB
    db = 20.0 * np.log10(rms_safe / ref_val)

    # Determine non-silent frames
    threshold_db = -top_db
    non_silent = db > threshold_db

    return non_silent