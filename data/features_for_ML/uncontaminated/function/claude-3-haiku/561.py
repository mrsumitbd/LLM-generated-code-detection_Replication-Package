def calc_recall(pred: Dict, gold: Dict, use_gold_for_eval: bool):
    """
    Calculates the recall metric for the given prediction and gold standard dictionaries.

    Args:
        pred (Dict): A dictionary containing the predicted values.
        gold (Dict): A dictionary containing the ground truth (gold standard) values.
        use_gold_for_eval (bool): If True, the gold standard dictionary is used for evaluation.
                                 If False, the prediction dictionary is used for evaluation.

    Returns:
        float: The recall metric value.
    """
    if use_gold_for_eval:
        true_positives = sum(1 for key in gold if key in pred and gold[key] == pred[key])
        total_positives = len(gold)
    else:
        true_positives = sum(1 for key in pred if key in gold and gold[key] == pred[key])
        total_positives = len(pred)

    recall = true_positives / total_positives if total_positives > 0 else 0.0
    return recall