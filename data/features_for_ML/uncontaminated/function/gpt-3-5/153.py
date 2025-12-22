def compute_score(solution_str, ground_truth) -> float:
    score = 0
    for i in range(len(solution_str)):
        if solution_str[i] == ground_truth[i]:
            score += 1
    return score / len(solution_str)