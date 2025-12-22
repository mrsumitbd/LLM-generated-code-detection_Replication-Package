def get_classification_metrics(pred_with_gt: list[Prediction]):
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    
    for pred in pred_with_gt:
        if pred.prediction == 1 and pred.ground_truth == 1:
            true_positives += 1
        elif pred.prediction == 1 and pred.ground_truth == 0:
            false_positives += 1
        elif pred.prediction == 0 and pred.ground_truth == 0:
            true_negatives += 1
        elif pred.prediction == 0 and pred.ground_truth == 1:
            false_negatives += 1
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }