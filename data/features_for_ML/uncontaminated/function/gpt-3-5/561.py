def calc_recall(pred: Dict, gold: Dict, use_gold_for_eval: bool):
    if use_gold_for_eval:
        relevant = 0
        total = 0
        for key in gold:
            total += len(gold[key])
            if key in pred:
                relevant += len(set(gold[key]) & set(pred[key]))
        if total == 0:
            return 0.0
        return relevant / total
    else:
        relevant = 0
        total = 0
        for key in pred:
            total += len(pred[key])
            if key in gold:
                relevant += len(set(gold[key]) & set(pred[key]))
        if total == 0:
            return 0.0
        return relevant / total