class Solution:
    
    @classmethod
    def validate(cls, node: TreeNode[int] | None, min_val: float, max_val: float) -> bool:
        if node is None:
            return True
        
        if not (min_val < node.val < max_val):
            return False
        
        return cls.validate(node.left, min_val, node.val) and cls.validate(node.right, node.val, max_val)
    
    def is_valid_bst(self, root: TreeNode[int] | None) -> bool:
        return self.validate(root, float('-inf'), float('inf'))