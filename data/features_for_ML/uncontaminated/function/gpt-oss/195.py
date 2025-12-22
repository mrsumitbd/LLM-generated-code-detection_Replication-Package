from typing import Sequence, List

def find_token(token_list: Sequence[int], token: str) -> Sequence[int]:
    """
    Return the indices of all occurrences of the integer value represented by `token`
    within `token_list`. If `token` cannot be converted to an integer, an empty
    sequence is returned.
    """
    try:
        target = int(token)
    except ValueError:
        return []

    indices: List[int] = []
    for idx, value in enumerate(token_list):
        if value == target:
            indices.append(idx)
    return indices