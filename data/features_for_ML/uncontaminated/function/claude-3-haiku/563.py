def _chunk_string(value: str, size: int) -> List[str]:
    """
    Splits a given string into a list of substrings, where each substring has a maximum length of `size`.

    Args:
        value (str): The input string to be chunked.
        size (int): The maximum length of each substring.

    Returns:
        List[str]: A list of substrings, where each substring has a maximum length of `size`.
    """
    return [value[i:i+size] for i in range(0, len(value), size)]