def run_can_attend_meetings(solution_class: type, intervals: list[list[int]]):
    solution = solution_class()
    result = solution.canAttendMeetings(intervals)
    print(result)