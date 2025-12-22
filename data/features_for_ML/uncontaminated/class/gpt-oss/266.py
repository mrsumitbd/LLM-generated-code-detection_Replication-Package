import heapq
from typing import List

class Solution:
    def k_closest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        Return the k points closest to the origin (0, 0) based on Euclidean distance.
        """
        # Use a min-heap to efficiently retrieve the k smallest distances.
        # heapq.nsmallest returns the k smallest elements according to the key.
        return heapq.nsmallest(k, points, key=lambda p: p[0] * p[0] + p[1] * p[1])