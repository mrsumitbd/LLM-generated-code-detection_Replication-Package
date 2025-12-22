def assert_climb_stairs(result: int, expected: int) -> bool:
    try:
        assert result == expected, f"Expected {expected}, but got {result}"
        return True
    except AssertionError as e:
        print(e)
        return False