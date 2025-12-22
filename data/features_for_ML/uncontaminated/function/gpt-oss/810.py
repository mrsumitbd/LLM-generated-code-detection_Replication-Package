def run_longest_consecutive(solution_class: type, nums: list[int]):
    """Run the longest consecutive sequence solver from the given solution class."""
    # Instantiate the solution class
    solution = solution_class()
    # Call the method that computes the longest consecutive sequence length
    # The expected method name is `longestConsecutive`. If the class uses a different
    # name, adjust accordingly.
    return solution.longestConsecutive(nums)