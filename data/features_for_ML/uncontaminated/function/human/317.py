from leetcode_py import TreeNode

def dfs(node: TreeNode[int] | None) -> int:
            nonlocal max_sum

            if not node:
                return 0

            # Get maximum path sum from left and right subtrees
            # If negative, we don't include them (take 0 instead)
            left_max = max(0, dfs(node.left))
            right_max = max(0, dfs(node.right))

            # Current path sum if this node is the highest point
            # (left path + current node + right path)
            current_path_sum = node.val + left_max + right_max

            # Update global maximum
            max_sum = max(max_sum, current_path_sum)

            # Return maximum path sum that can be extended upward
            # (either left or right path + current node)
            return node.val + max(left_max, right_max)