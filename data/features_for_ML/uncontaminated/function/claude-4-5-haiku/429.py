def assert_three_sum(result: list[list[int]], expected: list[list[int]]) -> bool:
    # Sort both result and expected for comparison since order doesn't matter
    result_sorted = sorted([sorted(triplet) for triplet in result])
    expected_sorted = sorted([sorted(triplet) for triplet in expected])
    return result_sorted == expected_sorted