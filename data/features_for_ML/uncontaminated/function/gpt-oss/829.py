def run_can_attend_meetings(solution_class: type, intervals: list[list[int]]):
    """
    Instantiate the provided solution class and invoke its `canAttendMeetings` method
    with the given list of intervals. The method is expected to return a boolean
    indicating whether the meetings can be attended without overlap.

    Parameters
    ----------
    solution_class : type
        The class that implements the `canAttendMeetings` method.
    intervals : list[list[int]]
        A list of [start, end] pairs representing meeting times.

    Returns
    -------
    bool
        The result of the `canAttendMeetings` method.
    """
    # Create an instance of the solution class
    solution = solution_class()

    # Ensure the method exists
    if not hasattr(solution, "canAttendMeetings"):
        raise AttributeError(
            f"{solution_class.__name__} does not implement 'canAttendMeetings' method."
        )

    # Call the method and return its result
    return solution.canAttendMeetings(intervals)