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
    # Compute the amplitude envelope
    if callable(ref):
        envelope = ref(y)
    else:
        envelope = np.abs(y)

    # Compute the power (squared amplitude) in decibels
    power = 10 * np.log10(envelope ** 2)

    # Aggregate power across channels
    if y.ndim > 1:
        power = np.apply_over_axes(aggregate, power, axes=tuple(range(1, y.ndim)))

    # Compute the non-silent indicator
    if top_db < 0:
        non_silent = power >= ref + abs(top_db)
    else:
        non_silent = power >= ref - top_db

    return non_silent