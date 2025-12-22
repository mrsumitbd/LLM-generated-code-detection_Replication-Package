def run_min_window(solution_class: type, s: str, t: str):
    solution = solution_class()
    result = solution.minWindow(s, t)
    print(f"Minimum window substring: {result}")