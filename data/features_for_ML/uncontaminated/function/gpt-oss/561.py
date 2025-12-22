from typing import Dict, Iterable, Set

def calc_recall(pred: Dict, gold: Dict, use_gold_for_eval: bool) -> float:
    """
    Calculate recall over a collection of predictions and gold labels.

    Parameters
    ----------
    pred : Dict
        Mapping from keys to an iterable of predicted items.
    gold : Dict
        Mapping from keys to an iterable of gold items.
    use_gold_for_eval : bool
        If True, use the gold set size as the denominator (standard recall).
        If False, use the predicted set size as the denominator (precision-like).

    Returns
    -------
    float
        The recall value (or precision-like value if use_gold_for_eval is False).
    """
    # Ensure we work with sets for efficient intersection
    def to_set(v: Iterable) -> Set:
        return set(v) if v is not None else set()

    correct = 0
    denom = 0

    # Consider all keys that appear in either dictionary
    all_keys = set(pred.keys()) | set(gold.keys())

    for key in all_keys:
        pred_set = to_set(pred.get(key, []))
        gold_set = to_set(gold.get(key, []))

        correct += len(pred_set & gold_set)
        denom += len(gold_set) if use_gold_for_eval else len(pred_set)

    return 0.0 if denom == 0 else correct / denom