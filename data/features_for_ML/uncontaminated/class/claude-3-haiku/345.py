class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        result = []
        self.backtrack(nums, [], result)
        return result

    def backtrack(self, nums, path, result):
        if not nums:
            result.append(path[:])
            return

        for i in range(len(nums)):
            path.append(nums[i])
            self.backtrack(nums[:i] + nums[i+1:], path, result)
            path.pop()