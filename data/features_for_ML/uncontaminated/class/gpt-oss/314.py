class Solution:
    def erase_overlap_intervals(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0
        intervals.sort(key=lambda x: x[1])
        count = 1
        prev_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start >= prev_end:
                count += 1
                prev_end = end
        return len(intervals) - count