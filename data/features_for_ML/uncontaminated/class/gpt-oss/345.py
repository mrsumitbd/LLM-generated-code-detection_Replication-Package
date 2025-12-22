class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        res: list[list[int]] = []
        n = len(nums)
        used = [False] * n
        path: list[int] = []

        def backtrack():
            if len(path) == n:
                res.append(path.copy())
                return
            for i in range(n):
                if not used[i]:
                    used[i] = True
                    path.append(nums[i])
                    backtrack()
                    path.pop()
                    used[i] = False

        backtrack()
        return res