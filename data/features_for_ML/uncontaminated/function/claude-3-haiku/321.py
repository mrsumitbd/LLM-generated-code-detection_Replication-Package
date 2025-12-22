from typing import List
from dataclasses import dataclass

@dataclass
class Prediction:
    label: str
    ground_truth: str

def get_classification_metrics(pred_with_gt: List[Prediction]):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0

    for prediction in pred_with_gt:
        if prediction.label == prediction.ground_truth:
            if prediction.label == 'positive':
                true_positives += 1
            else:
                true_negatives += 1
        else:
            if prediction.label == 'positive':
                false_positives += 1
            else:
                false_negatives += 1

    accuracy = (true_positives + true_negatives) / len(pred_with_gt)
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) != 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }