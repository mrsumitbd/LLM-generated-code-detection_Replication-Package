class Solution:
    
    def permute(self, nums: list[int]) -> list[list[int]]:
        def backtrack(curr_permutation, remaining_nums):
            if not remaining_nums:
                permutations.append(curr_permutation)
                return
            for i in range(len(remaining_nums)):
                new_permutation = curr_permutation + [remaining_nums[i]]
                new_remaining = remaining_nums[:i] + remaining_nums[i+1:]
                backtrack(new_permutation, new_remaining)
        
        permutations = []
        backtrack([], nums)
        return permutations