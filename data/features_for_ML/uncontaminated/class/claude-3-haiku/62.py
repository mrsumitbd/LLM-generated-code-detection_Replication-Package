class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        result = []
        self.backtrack(nums, 0, [], result)
        return result

    def backtrack(self, nums, start, subset, result):
        result.append(subset[:])
        for i in range(start, len(nums)):
            subset.append(nums[i])
            self.backtrack(nums, i + 1, subset, result)
            subset.pop()