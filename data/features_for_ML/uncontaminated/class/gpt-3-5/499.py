class Solution:
    
    def __init__(self, first_bad: int = 1) -> None:
        self.first_bad = first_bad

    def first_bad_version(self, n: int) -> int:
        left = 1
        right = n
        while left < right:
            mid = left + (right - left) // 2
            if isBadVersion(mid):
                right = mid
            else:
                left = mid + 1
        return left