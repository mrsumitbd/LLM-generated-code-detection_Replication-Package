def evaluate_dicts(pred: List[Dict], gold: List[Dict]):
    pred_set = set((tuple(sorted(d.items())) for d in pred))
    gold_set = set((tuple(sorted(d.items())) for d in gold))
    
    true_positives = len(pred_set.intersection(gold_set))
    false_positives = len(pred_set.difference(gold_set))
    false_negatives = len(gold_set.difference(pred_set))
    
    precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    
    return precision, recall, f1_score