from typing import Literal, Optional, TypedDict, Dict, Any, List, Tuple

def split_array(array: List[Any], splits: List[int]):
    """
    Split band and kline by incontinuous points
    """
    splited_array = []
    for i in range(len(splits)):
        if i == 0:
            start = 0
        else:
            start = splits[i-1]
        
        if i == len(splits) - 1:
            end = splits[-1]
        else:
            end = splits[i]
        
        splited_array.append(array[start:end])
    
    splited_array.append(array[splits[-1]:])
    return splited_array