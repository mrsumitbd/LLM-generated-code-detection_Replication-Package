def compute_score(solution_str, ground_truth) -> float:
    """
    Compute a similarity score between `solution_str` and `ground_truth`.
    The score is a float in the range [0.0, 1.0] representing the Jaccard
    similarity of the token sets derived from the two strings.

    Parameters
    ----------
    solution_str : str
        The string produced by the solution.
    ground_truth : str
        The reference string to compare against.

    Returns
    -------
    float
        Jaccard similarity between the token sets of the two strings.
    """
    # Normalize whitespace and split into tokens
    tokens_solution = set(solution_str.strip().split())
    tokens_truth = set(ground_truth.strip().split())

    # Handle the degenerate case where both are empty
    if not tokens_solution and not tokens_truth:
        return 1.0

    # Compute intersection and union
    intersection = tokens_solution & tokens_truth
    union = tokens_solution | tokens_truth

    # Avoid division by zero
    if not union:
        return 0.0

    return len(intersection) / len(union)