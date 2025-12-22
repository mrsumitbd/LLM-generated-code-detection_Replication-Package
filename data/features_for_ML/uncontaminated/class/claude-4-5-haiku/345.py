class Solution:

    def permute(self, nums: list[int]) -> list[list[int]]:
        result = []
        
        def backtrack(current):
            if len(current) == len(nums):
                result.append(current[:])
                return
            
            for num in nums:
                if num not in current:
                    current.append(num)
                    backtrack(current)
                    current.pop()
        
        backtrack([])
        return result