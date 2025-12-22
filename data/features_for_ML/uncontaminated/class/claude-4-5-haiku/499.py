class Solution:

    def __init__(self, first_bad: int = 1) -> None:
        self.first_bad = first_bad

    def first_bad_version(self, n: int) -> int:
        left, right = 1, n
        
        while left < right:
            mid = left + (right - left) // 2
            if mid < self.first_bad:
                left = mid + 1
            else:
                right = mid
        
        return left