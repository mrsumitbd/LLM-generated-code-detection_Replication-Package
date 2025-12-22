def assert_lowest_common_ancestor(result: TreeNode[int] | None, expected_val: int) -> bool:
    if result is None:
        return False
    return result.val == expected_val