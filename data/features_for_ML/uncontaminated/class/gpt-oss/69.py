class Solution:
    def group_anagrams(self, strs: list[str]) -> list[list[str]]:
        from collections import defaultdict
        anagrams = defaultdict(list)
        for s in strs:
            key = tuple(sorted(s))
            anagrams[key].append(s)
        return list(anagrams.values())