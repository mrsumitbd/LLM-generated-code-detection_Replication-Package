def split_array(array: List[Any], splits: List[int]):
    """
    Split band and kline by incontinuous points
    """
    if not splits or not array:
        return [array]
    
    result = []
    start = 0
    
    for split_point in sorted(splits):
        if split_point > start:
            result.append(array[start:split_point])
        start = split_point
    
    if start < len(array):
        result.append(array[start:])
    
    return result