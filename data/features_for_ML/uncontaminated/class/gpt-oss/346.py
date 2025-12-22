from __future__ import annotations
from typing import Optional, Iterator

class TreeNode:
    def __init__(self, val: int, left: Optional['TreeNode']=None, right: Optional['TreeNode']=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def __init__(self) -> None:
        pass

    def serialize(self, root: Optional[TreeNode]) -> str:
        """Serialize a binary tree to a string using preorder traversal."""
        def helper(node: Optional[TreeNode]) -> None:
            if node is None:
                parts.append('#')
                return
            parts.append(str(node.val))
            helper(node.left)
            helper(node.right)

        parts: list[str] = []
        helper(root)
        return ','.join(parts)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Deserialize a string back into a binary tree."""
        def helper(it: Iterator[str]) -> Optional[TreeNode]:
            val = next(it)
            if val == '#':
                return None
            node = TreeNode(int(val))
            node.left = helper(it)
            node.right = helper(it)
            return node

        if not data:
            return None
        it = iter(data.split(','))
        return helper(it)