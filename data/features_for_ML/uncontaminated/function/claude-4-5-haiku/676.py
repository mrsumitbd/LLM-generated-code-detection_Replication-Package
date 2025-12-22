def amplitude_to_db(
    S,
    *,
    ref: float | Callable = 1.0,
    amin: float = 1e-5,
    top_db: float | None = 80.0,
) -> np.floating[Any] | np.ndarray:
    """Convert an amplitude spectrogram to dB-scaled spectrogram.

    This is equivalent to ``power_to_db(S**2, ref=ref**2, amin=amin**2, top_db=top_db)``,
    but is provided for convenience.

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

    See Also
    --------
    power_to_db, db_to_amplitude

    Notes
    -----
    This function caches at level 30.
    """
    S = np.asarray(S)
    
    # Compute reference value
    if callable(ref):
        ref_value = ref(S)
    else:
        ref_value = ref
    
    # Apply minimum threshold
    S = np.maximum(amin, np.abs(S))
    ref_value = np.maximum(amin, np.asarray(ref_value))
    
    # Convert to dB: 20 * log10(S / ref)
    S_db = 20.0 * np.log10(S / ref_value)
    
    # Apply top_db threshold if specified
    if top_db is not None:
        if S_db.ndim > 0:
            peak = np.max(S_db)
        else:
            peak = S_db
        S_db = np.maximum(S_db, peak - top_db)
    
    return S_db