def assert_lowest_common_ancestor(result: TreeNode[int] | None, expected_val: int) -> bool:
    """
    Return True if the given result is a TreeNode whose value equals expected_val.
    Otherwise return False.
    """
    if result is None:
        return False
    try:
        return result.val == expected_val
    except AttributeError:
        return False