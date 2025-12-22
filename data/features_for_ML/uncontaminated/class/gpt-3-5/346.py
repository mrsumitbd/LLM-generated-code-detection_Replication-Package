from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:

    def serialize(self, root: TreeNode[int] | None) -> str:
        if not root:
            return 'None'
        return str(root.val) + ',' + self.serialize(root.left) + ',' + self.serialize(root.right)

    def deserialize(self, data: str) -> TreeNode[int] | None:
        def build_tree(nodes):
            val = next(nodes)
            if val == 'None':
                return None
            node = TreeNode(int(val))
            node.left = build_tree(nodes)
            node.right = build_tree(nodes)
            return node

        nodes = iter(data.split(','))
        return build_tree(nodes)