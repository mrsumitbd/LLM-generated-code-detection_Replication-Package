from __future__ import annotations
from typing import Optional

class Solution:
    @classmethod
    def validate(cls, node: Optional[TreeNode[int]], min_val: float, max_val: float) -> bool:
        if node is None:
            return True
        if not (min_val < node.val < max_val):
            return False
        return (
            cls.validate(node.left, min_val, node.val) and
            cls.validate(node.right, node.val, max_val)
        )

    def is_valid_bst(self, root: Optional[TreeNode[int]]) -> bool:
        return self.validate(root, float('-inf'), float('inf'))