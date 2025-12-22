class Solution:

    def __init__(self, first_bad: int = 1) -> None:
        self.first_bad = first_bad

    def first_bad_version(self, n: int) -> int:
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if mid >= self.first_bad:
                hi = mid
            else:
                lo = mid + 1
        return lo