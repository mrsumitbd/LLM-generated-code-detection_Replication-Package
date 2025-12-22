class Solution:

    def group_anagrams(self, strs: list[str]) -> list[list[str]]:
        anagram_map = {}
        
        for word in strs:
            sorted_word = ''.join(sorted(word))
            
            if sorted_word not in anagram_map:
                anagram_map[sorted_word] = []
            
            anagram_map[sorted_word].append(word)
        
        return list(anagram_map.values())