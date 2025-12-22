def assert_three_sum(result: list[list[int]], expected: list[list[int]]) -> bool:
    result.sort()
    expected.sort()
    return result == expected