def evaluate(pred, target, metrics, id2type):
    """
    Evaluates the performance of a model on a given dataset.

    Args:
        pred (list): A list of predicted values.
        target (list): A list of ground truth values.
        metrics (list): A list of metric functions to be used for evaluation.
        id2type (dict): A dictionary mapping entity IDs to their corresponding types.

    Returns:
        dict: A dictionary containing the evaluation results for each metric.
    """
    results = {}
    for metric in metrics:
        results[metric.__name__] = metric(pred, target, id2type)
    return results