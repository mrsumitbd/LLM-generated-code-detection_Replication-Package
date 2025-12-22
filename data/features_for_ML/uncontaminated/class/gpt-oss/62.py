class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        result: list[list[int]] = [[]]
        for num in nums:
            result += [curr + [num] for curr in result]
        return result