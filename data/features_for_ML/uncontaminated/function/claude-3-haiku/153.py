def compute_score(solution_str, ground_truth) -> float:
    if len(solution_str) != len(ground_truth):
        return 0.0

    correct_count = 0
    for i in range(len(solution_str)):
        if solution_str[i] == ground_truth[i]:
            correct_count += 1

    return correct_count / len(solution_str)