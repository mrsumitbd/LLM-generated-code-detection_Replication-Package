class Solution:
    def k_closest(self, points: list[list[int]], k: int) -> list[list[int]]:
        distances = [(x**2 + y**2, x, y) for x, y in points]
        distances.sort()
        return [[x, y] for _, x, y in distances[:k]]