class Solution:
    
    def subsets(self, nums: list[int]) -> list[list[int]]:
        def backtrack(start, path, result):
            result.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path, result)
                path.pop()
        
        result = []
        backtrack(0, [], result)
        return result