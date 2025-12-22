def dfs(node: TreeNode[int] | None) -> int:
    if node is None:
        return 0
    
    left_sum = dfs(node.left)
    right_sum = dfs(node.right)
    
    return node.val + left_sum + right_sum