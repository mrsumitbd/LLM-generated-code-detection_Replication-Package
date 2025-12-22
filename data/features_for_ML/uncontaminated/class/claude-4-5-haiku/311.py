class Solution:

    def alien_order(self, words: list[str]) -> str:
        # Build the graph and in-degree count
        graph = {char: set() for word in words for char in word}
        in_degree = {char: 0 for word in words for char in word}
        
        # Compare adjacent words to find ordering
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            min_len = min(len(word1), len(word2))
            
            # If word1 is longer and word2 is a prefix, invalid order
            if len(word1) > len(word2) and word1[:min_len] == word2[:min_len]:
                return ""
            
            # Find first different character
            for j in range(min_len):
                if word1[j] != word2[j]:
                    if word2[j] not in graph[word1[j]]:
                        graph[word1[j]].add(word2[j])
                        in_degree[word2[j]] += 1
                    break
        
        # Topological sort using Kahn's algorithm
        queue = [char for char in graph if in_degree[char] == 0]
        result = []
        
        while queue:
            char = queue.pop(0)
            result.append(char)
            
            for neighbor in graph[char]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # If not all characters are in result, there's a cycle
        if len(result) != len(graph):
            return ""
        
        return "".join(result)