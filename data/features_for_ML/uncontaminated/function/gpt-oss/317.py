def dfs(node: "TreeNode[int]" | None) -> int:
    """
    Perform a depth‑first traversal of a binary tree and return the sum of all node values.
    """
    if node is None:
        return 0
    return node.val + dfs(node.left) + dfs(node.right)