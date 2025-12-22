from typing import List, Any

def split_array(array: List[Any], splits: List[int]) -> List[List[Any]]:
    """
    Split an array into sub‑arrays at the positions specified in `splits`.

    Parameters
    ----------
    array : List[Any]
        The original list to be split.
    splits : List[int]
        Indices at which to split the array. Each index `i` indicates that a new
        sub‑array should start at position `i`. The indices are interpreted as
        positions in the original array (0‑based). Duplicate or out‑of‑range
        indices are ignored. The list is sorted internally.

    Returns
    -------
    List[List[Any]]
        A list of sub‑arrays resulting from the split. If `splits` is empty,
        the result is a single element list containing the original array.
    """
    if not array:
        return []

    # Filter valid splits and sort them
    valid_splits = sorted({i for i in splits if 0 < i < len(array)})

    result: List[List[Any]] = []
    start = 0
    for idx in valid_splits:
        result.append(array[start:idx])
        start = idx
    result.append(array[start:])  # tail segment

    return result