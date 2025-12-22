def evaluate(pred, target, metrics, id2type):
    """
    Evaluate predictions against targets using the specified metrics.

    Parameters
    ----------
    pred : list
        List of predictions. Each element can be an int, a list/tuple of ints,
        or a string. If an int or string is provided, it is treated as a
        single-label prediction.
    target : list
        List of ground‑truth labels. Each element can be an int, a list/tuple
        of ints, or a string. If an int or string is provided, it is treated
        as a single-label target.
    metrics : list of str
        Names of metrics to compute. Supported names are:
        - 'accuracy'   : exact‑match accuracy
        - 'precision'  : micro‑averaged precision
        - 'recall'     : micro‑averaged recall
        - 'f1'         : micro‑averaged F1 score
    id2type : dict or None
        Optional mapping from numeric ids to type names. If provided, all
        numeric ids in `pred` and `target` are converted to the corresponding
        type names before evaluation.

    Returns
    -------
    dict
        Dictionary mapping metric names to their computed values.
    """
    # Helper to normalise a single element into a set of labels
    def _to_set(x):
        if isinstance(x, (list, tuple, set)):
            return set(x)
        # treat string as a single label
        return {x}

    # Convert numeric ids to type names if mapping is provided
    if id2type is not None:
        def _convert(item):
            if isinstance(item, (list, tuple, set)):
                return {id2type.get(v, v) for v in item}
            return id2type.get(item, item)
    else:
        _convert = lambda x: x

    # Normalise predictions and targets
    preds = [_to_set(_convert(p)) for p in pred]
    trgs  = [_to_set(_convert(t)) for t in target]

    # Basic checks
    if len(preds) != len(trgs):
        raise ValueError("Length of predictions and targets must match.")

    # Compute exact‑match accuracy
    results = {}
    if 'accuracy' in metrics:
        correct = sum(1 for p, t in zip(preds, trgs) if p == t)
        results['accuracy'] = correct / len(preds) if preds else 0.0

    # Compute micro‑averaged precision, recall, f1
    if any(m in metrics for m in ('precision', 'recall', 'f1')):
        tp = fp = fn = 0
        for p, t in zip(preds, trgs):
            tp += len(p & t)
            fp += len(p - t)
            fn += len(t - p)

        if 'precision' in metrics:
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            results['precision'] = precision

        if 'recall' in metrics:
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            results['recall'] = recall

        if 'f1' in metrics:
            prec = results.get('precision', tp / (tp + fp) if (tp + fp) > 0 else 0.0)
            rec  = results.get('recall',   tp / (tp + fn) if (tp + fn) > 0 else 0.0)
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
            results['f1'] = f1

    return results