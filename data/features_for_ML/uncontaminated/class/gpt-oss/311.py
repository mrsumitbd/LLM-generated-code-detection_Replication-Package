class Solution:
    def alien_order(self, words: list[str]) -> str:
        from collections import defaultdict, deque

        # Build graph
        graph = defaultdict(set)  # node -> set of neighbors
        indegree = defaultdict(int)
        nodes = set()

        # Initialize nodes and indegree
        for word in words:
            for ch in word:
                nodes.add(ch)
                if ch not in indegree:
                    indegree[ch] = 0

        # Add edges
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            min_len = min(len(w1), len(w2))
            diff_found = False
            for j in range(min_len):
                c1, c2 = w1[j], w2[j]
                if c1 != c2:
                    if c2 not in graph[c1]:
                        graph[c1].add(c2)
                        indegree[c2] += 1
                    diff_found = True
                    break
            if not diff_found and len(w1) > len(w2):
                return ""

        # Topological sort (Kahn)
        queue = deque([node for node in nodes if indegree[node] == 0])
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for neigh in graph[node]:
                indegree[neigh] -= 1
                if indegree[neigh] == 0:
                    queue.append(neigh)

        if len(order) != len(nodes):
            return ""
        return "".join(order)