def run_rob(solution_class: type, nums: list[int]):
    """Instantiate the given solution class and run its `rob` method on `nums`."""
    # Create an instance of the solution class
    solution = solution_class()
    # Call the `rob` method and return the result
    return solution.rob(nums)