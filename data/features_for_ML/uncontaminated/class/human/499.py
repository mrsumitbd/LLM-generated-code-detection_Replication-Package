
class Solution:

    def __init__(self, first_bad: int = 1) -> None:
        self.is_bad_version = lambda version: version >= first_bad

    # Time: O(log n)
    # Space: O(1)
    def first_bad_version(self, n: int) -> int:
        left = 1
        right = n

        while left < right:
            mid = (left + right) // 2
            if self.is_bad_version(mid):
                right = mid
            else:
                left = mid + 1

        return right