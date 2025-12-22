def assert_lowest_common_ancestor(result: TreeNode[int] | None, expected_val: int) -> bool:
    if result is None:
        return False
    if result.val == expected_val:
        return True
    left_result = assert_lowest_common_ancestor(result.left, expected_val)
    right_result = assert_lowest_common_ancestor(result.right, expected_val)
    return left_result or right_result