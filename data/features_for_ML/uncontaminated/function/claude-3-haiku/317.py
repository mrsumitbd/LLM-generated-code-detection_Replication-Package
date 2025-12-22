def dfs(node: TreeNode[int] | None) -> int:
    if not node:
        return 0
    
    left_sum = dfs(node.left)
    right_sum = dfs(node.right)
    
    return node.val + left_sum + right_sum