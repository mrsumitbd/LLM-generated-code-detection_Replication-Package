def assert_three_sum(result: list[list[int]], expected: list[list[int]]) -> bool:
    # Sort both result and expected for comparison since order doesn't matter
    result = [sorted(triplet) for triplet in result]
    expected = [sorted(triplet) for triplet in expected]

    # Check if the sorted results match the sorted expected output
    return set(map(tuple, result)) == set(map(tuple, expected))