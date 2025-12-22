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
    # Frame the signal
    frames = librosa.util.frame(y, frame_length=frame_length, hop_length=hop_length)
    
    # Compute power
    power = np.mean(frames ** 2, axis=0)
    
    # Get reference value
    if callable(ref):
        ref_value = ref(power)
    else:
        ref_value = ref
    
    # Convert to dB
    db = librosa.power_to_db(power, ref=ref_value)
    
    # Aggregate across channels if needed
    if db.ndim > 1:
        db = np.apply_over_axes(aggregate, db, axes=range(db.ndim - 1))
        db = db.squeeze()
    
    # Determine non-silent frames
    non_silent = db > -top_db
    
    return non_silent