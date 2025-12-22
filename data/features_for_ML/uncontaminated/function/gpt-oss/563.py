from typing import List

def _chunk_string(value: str, size: int) -> List[str]:
    """
    Split the input string `value` into a list of substrings each of length `size`.
    The last substring may be shorter if the string length is not a multiple of `size`.
    """
    if size <= 0:
        raise ValueError("size must be a positive integer")
    return [value[i:i + size] for i in range(0, len(value), size)]