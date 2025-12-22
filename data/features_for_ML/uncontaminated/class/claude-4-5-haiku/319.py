class Solution:

    def find_min_height_trees(self, n: int, edges: list[list[int]]) -> list[int]:
        if n == 1:
            return [0]
        
        # Build adjacency list and calculate degrees
        adj = [set() for _ in range(n)]
        degree = [0] * n
        
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
            degree[u] += 1
            degree[v] += 1
        
        # Find all leaf nodes (degree 1)
        leaves = [i for i in range(n) if degree[i] == 1]
        
        # Topologically remove leaves layer by layer
        remaining = n
        while remaining > 2:
            new_leaves = []
            for leaf in leaves:
                for neighbor in adj[leaf]:
                    degree[neighbor] -= 1
                    if degree[neighbor] == 1:
                        new_leaves.append(neighbor)
                remaining -= 1
            leaves = new_leaves
        
        return leaves if remaining == 2 else [i for i in range(n) if degree[i] >= 0][:remaining]