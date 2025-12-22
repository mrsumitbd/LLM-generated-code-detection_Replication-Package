from typing import List, Dict, Any

def evaluate_dicts(pred: List[Dict[Any, Any]], gold: List[Dict[Any, Any]]) -> Dict[str, float]:
    """
    Evaluate a list of predicted dictionaries against a list of gold dictionaries.

    The evaluation computes:
        - exact_match: fraction of dictionaries that match exactly.
        - precision: average precision over all dictionaries.
        - recall: average recall over all dictionaries.
        - f1: average F1 score over all dictionaries.

    Parameters
    ----------
    pred : List[Dict[Any, Any]]
        List of predicted dictionaries.
    gold : List[Dict[Any, Any]]
        List of gold dictionaries.

    Returns
    -------
    Dict[str, float]
        Dictionary containing the metrics.
    """
    if len(pred) != len(gold):
        raise ValueError("pred and gold must have the same length")

    total = len(pred)
    exact_matches = 0
    total_precision = 0.0
    total_recall = 0.0
    total_f1 = 0.0

    for p_dict, g_dict in zip(pred, gold):
        # Exact match
        if p_dict == g_dict:
            exact_matches += 1

        # Convert to sets of (key, value) tuples for comparison
        p_items = set(p_dict.items())
        g_items = set(g_dict.items())

        intersection = p_items & g_items
        inter_len = len(intersection)
        p_len = len(p_items)
        g_len = len(g_items)

        # Precision
        if p_len > 0:
            precision = inter_len / p_len
        else:
            precision = 1.0 if g_len == 0 else 0.0

        # Recall
        if g_len > 0:
            recall = inter_len / g_len
        else:
            recall = 1.0 if p_len == 0 else 0.0

        # F1
        if precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0.0

        total_precision += precision
        total_recall += recall
        total_f1 += f1

    return {
        "exact_match": exact_matches / total,
        "precision": total_precision / total,
        "recall": total_recall / total,
        "f1": total_f1 / total,
    }