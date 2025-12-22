def masked_max(*args, **kwargs):
    """
    Return the maximum value(s) from the provided iterable(s), optionally ignoring
    masked entries.

    Parameters
    ----------
    *args
        One or more iterable objects (lists, tuples, etc.). If a single iterable
        is provided, the maximum of its elements is returned. If multiple
        iterables are provided, the function returns an element‑wise maximum
        across them.
    **kwargs
        mask : iterable of bool
            Optional mask of the same length as the iterables. Elements
            corresponding to ``True`` in the mask are ignored when computing
            the maximum. For element‑wise operations, a masked position
            results in ``None`` in the output list.

    Returns
    -------
    scalar or list
        The maximum value if a single iterable is supplied, otherwise a list
        of element‑wise maxima. If all values are masked, ``None`` is returned
        for that position (or for the scalar case if all values are masked).

    Raises
    ------
    TypeError
        If no arguments are supplied.
    ValueError
        If the provided iterables are of differing lengths.
    """
    if not args:
        raise TypeError("masked_max requires at least one positional argument")

    mask = kwargs.get("mask", None)

    # Helper to validate mask length
    def _validate_mask(seq_len):
        if mask is None:
            return
        if len(mask) != seq_len:
            raise ValueError("mask length must match the length of the iterables")

    # Single iterable case
    if len(args) == 1:
        seq = args[0]
        seq_len = len(seq)
        _validate_mask(seq_len)

        if mask is None:
            # No mask: simple max
            return max(seq)
        else:
            # Apply mask
            filtered = [v for v, m in zip(seq, mask) if not m]
            return max(filtered) if filtered else None

    # Multiple iterables: element‑wise max
    seq_lengths = [len(a) for a in args]
    if len(set(seq_lengths)) != 1:
        raise ValueError("All iterables must have the same length")
    seq_len = seq_lengths[0]
    _validate_mask(seq_len)

    result = []
    for idx, vals in enumerate(zip(*args)):
        if mask is not None and mask[idx]:
            result.append(None)
        else:
            result.append(max(vals))
    return result