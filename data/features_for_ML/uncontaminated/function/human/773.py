import numpy as np
from collections.abc import Callable

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
    # Compute the MSE for the signal
    mse = rms(y=y, frame_length=frame_length, hop_length=hop_length)

    # Convert to decibels and slice out the mse channel
    db: np.ndarray = amplitude_to_db(mse[..., 0, :], ref=ref, top_db=None)

    # Aggregate everything but the time dimension
    if db.ndim > 1:
        db = np.apply_over_axes(aggregate, db, range(db.ndim - 1))
        # Squeeze out leading singleton dimensions here
        # We always want to keep the trailing dimension though
        db = np.squeeze(db, axis=tuple(range(db.ndim - 1)))

    return db > -top_db