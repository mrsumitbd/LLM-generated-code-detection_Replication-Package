from leetcode_py import TreeNode

def assert_lowest_common_ancestor(result: TreeNode[int] | None, expected_val: int) -> bool:
    assert result is not None
    assert result.val == expected_val
    return True