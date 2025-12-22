class SolutionMath:
    def unique_paths(self, m: int, n: int) -> int:
        # Use combinatorial formula: C(m+n-2, m-1)
        from math import comb
        return comb(m + n - 2, m - 1)