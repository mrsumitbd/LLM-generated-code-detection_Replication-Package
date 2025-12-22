from collections import deque
from typing import List

class Solution:
    def find_min_height_trees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n == 1:
            return [0]

        # Build adjacency list and degree count
        adj = [[] for _ in range(n)]
        degree = [0] * n
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
            degree[u] += 1
            degree[v] += 1

        # Initialize first layer of leaves
        leaves = deque([i for i in range(n) if degree[i] == 1])

        remaining_nodes = n
        while remaining_nodes > 2:
            leaves_count = len(leaves)
            remaining_nodes -= leaves_count
            for _ in range(leaves_count):
                leaf = leaves.popleft()
                for neighbor in adj[leaf]:
                    degree[neighbor] -= 1
                    if degree[neighbor] == 1:
                        leaves.append(neighbor)

        return list(leaves)