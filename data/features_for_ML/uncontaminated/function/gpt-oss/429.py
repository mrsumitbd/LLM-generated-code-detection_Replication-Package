def assert_three_sum(result: list[list[int]], expected: list[list[int]]) -> bool:
    """
    Compare two lists of integer triplets for equality, ignoring order of triplets
    and order within each triplet.

    Parameters
    ----------
    result : list[list[int]]
        The list of triplets produced by the algorithm.
    expected : list[list[int]]
        The list of triplets that are expected.

    Returns
    -------
    bool
        True if both lists contain the same triplets (ignoring order), False otherwise.
    """
    # Normalize each triplet by sorting its elements
    normalized_result = [sorted(triplet) for triplet in result]
    normalized_expected = [sorted(triplet) for triplet in expected]

    # Sort the list of triplets lexicographically
    normalized_result.sort()
    normalized_expected.sort()

    return normalized_result == normalized_expected