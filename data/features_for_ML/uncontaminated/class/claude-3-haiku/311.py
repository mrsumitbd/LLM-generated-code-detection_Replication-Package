from collections import defaultdict, deque

class Solution:
    def alien_order(self, words: list[str]) -> str:
        # Step 1: Create the graph and in-degree count
        graph = defaultdict(set)
        in_degree = {c: 0 for word in words for c in word}

        for i in range(1, len(words)):
            word1, word2 = words[i-1], words[i]
            for c1, c2 in zip(word1, word2):
                if c1 != c2:
                    if c2 not in graph[c1]:
                        graph[c1].add(c2)
                        in_degree[c2] += 1
                    break
            else:
                if len(word1) > len(word2):
                    return ""

        # Step 2: Topological sort
        queue = deque([c for c in in_degree if in_degree[c] == 0])
        result = []

        while queue:
            c = queue.popleft()
            result.append(c)
            for neighbor in graph[c]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Step 3: Check if the result is complete
        if len(result) != len(in_degree):
            return ""
        return "".join(result)