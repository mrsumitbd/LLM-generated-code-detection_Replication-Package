class Solution:

    def k_closest(self, points: list[list[int]], k: int) -> list[list[int]]:
        import heapq
        
        # Calculate distance squared for each point and create a min heap
        # We use negative distance to simulate a max heap for easier k-closest selection
        heap = []
        
        for point in points:
            dist_sq = point[0] ** 2 + point[1] ** 2
            heapq.heappush(heap, (-dist_sq, point))
            
            # Keep only k elements in the heap
            if len(heap) > k:
                heapq.heappop(heap)
        
        # Extract points from heap
        result = [point for _, point in heap]
        return result