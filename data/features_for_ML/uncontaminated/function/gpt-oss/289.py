def run_min_window(solution_class: type, s: str, t: str):
    """
    Instantiate the provided solution class and invoke its `minWindow` method
    with the given strings `s` and `t`. The result is returned.
    """
    # Create an instance of the solution class
    solution = solution_class()
    
    # Call the minWindow method (assumed to exist)
    result = solution.minWindow(s, t)
    
    # Return the result
    return result