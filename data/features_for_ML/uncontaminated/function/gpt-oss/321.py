from collections import defaultdict
from typing import List, Dict, Any

def get_classification_metrics(pred_with_gt: List[Any]) -> Dict[str, Any]:
    """
    Compute classification metrics for a list of predictions with ground truth.

    Each element in `pred_with_gt` is expected to have attributes `pred` and `gt`
    (or `prediction` and `ground_truth`). The function is tolerant to either
    naming convention.

    Returns a dictionary containing:
        - accuracy
        - per-class precision, recall, f1
        - macro-averaged precision, recall, f1
        - micro-averaged precision, recall, f1
        - confusion matrix (dict of dict)
    """
    # Helper to extract pred and gt
    def _get_values(item):
        if hasattr(item, "pred"):
            return item.pred, getattr(item, "gt", None)
        if hasattr(item, "prediction"):
            return getattr(item, "prediction", None), getattr(item, "ground_truth", None)
        raise AttributeError("Item must have 'pred' or 'prediction' attribute")

    # Gather all classes
    classes = set()
    for item in pred_with_gt:
        pred, gt = _get_values(item)
        classes.add(pred)
        classes.add(gt)

    # Initialize confusion matrix
    cm = {c: defaultdict(int) for c in classes}
    for item in pred_with_gt:
        pred, gt = _get_values(item)
        cm[gt][pred] += 1

    # Compute per-class metrics
    per_class = {}
    total_correct = 0
    total_samples = 0
    tp_total = 0
    fp_total = 0
    fn_total = 0

    for cls in classes:
        tp = cm[cls].get(cls, 0)
        fp = sum(cm[other].get(cls, 0) for other in classes if other != cls)
        fn = sum(cm[cls].get(other, 0) for other in classes if other != cls)
        tn = sum(cm[other].get(other2, 0)
                for other in classes for other2 in classes
                if other != cls and other2 != cls)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        per_class[cls] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
        }

        total_correct += tp
        total_samples += tp + fp + fn + tn
        tp_total += tp
        fp_total += fp
        fn_total += fn

    # Accuracy
    accuracy = total_correct / total_samples if total_samples > 0 else 0.0

    # Macro-averaged metrics
    macro_precision = sum(v["precision"] for v in per_class.values()) / len(classes) if classes else 0.0
    macro_recall = sum(v["recall"] for v in per_class.values()) / len(classes) if classes else 0.0
    macro_f1 = sum(v["f1"] for v in per_class.values()) / len(classes) if classes else 0.0

    # Micro-averaged metrics
    micro_precision = tp_total / (tp_total + fp_total) if (tp_total + fp_total) > 0 else 0.0
    micro_recall = tp_total / (tp_total + fn_total) if (tp_total + fn_total) > 0 else 0.0
    micro_f1 = (2 * micro_precision * micro_recall) / (micro_precision + micro_recall) if (micro_precision + micro_recall) > 0 else 0.0

    # Convert confusion matrix to plain dict of dicts
    cm_dict = {str(k): {str(k2): v for k2, v in v2.items()} for k, v2 in cm.items()}

    return {
        "accuracy": accuracy,
        "per_class": per_class,
        "macro_precision": macro_precision,
        "macro_recall": macro_recall,
        "macro_f1": macro_f1,
        "micro_precision": micro_precision,
        "micro_recall": micro_recall,
        "micro_f1": micro_f1,
        "confusion_matrix": cm_dict,
    }