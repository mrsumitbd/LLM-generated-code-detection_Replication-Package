class Codec:

    def __init__(self) -> None:
        pass

    def serialize(self, root: TreeNode[int] | None) -> str:
        def dfs(node):
            if not node:
                result.append("None")
                return
            result.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        
        result = []
        dfs(root)
        return ",".join(result)

    def deserialize(self, data: str) -> TreeNode[int] | None:
        def dfs(nodes):
            val = next(nodes)
            if val == "None":
                return None
            node = TreeNode(int(val))
            node.left = dfs(nodes)
            node.right = dfs(nodes)
            return node
        
        nodes = iter(data.split(","))
        return dfs(nodes)