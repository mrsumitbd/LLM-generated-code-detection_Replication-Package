def split_array(array: List[Any], splits: List[int]):
    """
    Split band and kline by incontinuous points
    """
    result = []
    start = 0
    for split in splits:
        result.append(array[start:split])
        start = split
    result.append(array[start:])
    return result