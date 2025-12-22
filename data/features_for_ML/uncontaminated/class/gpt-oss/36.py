class Solution:
    def can_attend_meetings(self, intervals: list[list[int]]) -> bool:
        if not intervals:
            return True
        # Sort intervals by start time
        intervals.sort(key=lambda x: x[0])
        # Check for any overlap
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i-1][1]:
                return False
        return True