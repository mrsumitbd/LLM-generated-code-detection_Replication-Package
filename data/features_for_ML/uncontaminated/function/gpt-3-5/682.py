from typing import List, Any

def split_array(array: List[Any], splits: List[int]):
    result = []
    start = 0
    for split in splits:
        result.append(array[start:split])
        start = split
    result.append(array[start:])
    return result