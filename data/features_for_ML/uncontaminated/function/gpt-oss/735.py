def __compress(result, target: str, power: int):
    """
    Compresses the input string `target` using a simple run‑length encoding
    scheme and appends the compressed representation to the `result`
    sequence.  Consecutive runs of the same character are replaced by
    ``<char><count>`` only if the run length is at least `power`.  If the
    run length is smaller than `power`, the original characters are
    appended unchanged.

    Parameters
    ----------
    result : list
        A mutable sequence to which the compressed fragments are appended.
    target : str
        The string to be compressed.
    power : int
        The minimum run length required to encode a run.  Runs shorter
        than this value are left as literal characters.

    Returns
    -------
    None
    """
    i = 0
    n = len(target)
    while i < n:
        j = i + 1
        while j < n and target[j] == target[i]:
            j += 1
        count = j - i
        if count >= power:
            result.append(f"{target[i]}{count}")
        else:
            result.append(target[i] * count)
        i = j