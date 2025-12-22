class Solution:
    
    def alien_order(self, words: list[str]) -> str:
        graph = {}
        in_degree = {}
        
        for word in words:
            for char in word:
                graph[char] = set()
                in_degree[char] = 0
        
        for i in range(1, len(words)):
            word1 = words[i-1]
            word2 = words[i]
            found_diff = False
            
            for j in range(min(len(word1), len(word2))):
                if word1[j] != word2[j]:
                    if word2[j] not in graph[word1[j]]:
                        graph[word1[j]].add(word2[j])
                        in_degree[word2[j]] += 1
                    found_diff = True
                    break
            
            if not found_diff and len(word1) > len(word2):
                return ""
        
        result = []
        queue = [char for char in in_degree if in_degree[char] == 0]
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) < len(in_degree):
            return ""
        
        return "".join(result)