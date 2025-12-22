from __future__ import annotations
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def dfs(node: TreeNode[int] | None) -> int:
    if not node:
        return 0
    return node.val + dfs(node.left) + dfs(node.right)