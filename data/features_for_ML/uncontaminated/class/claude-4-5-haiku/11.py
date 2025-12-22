class Solution:

    def contains_duplicate(self, nums: list[int]) -> bool:
        return len(nums) != len(set(nums))