def get_classification_metrics(pred_with_gt: list[Prediction]):
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
    
    if not pred_with_gt:
        return {}
    
    y_true = [p.ground_truth for p in pred_with_gt]
    y_pred = [p.prediction for p in pred_with_gt]
    
    # Determine if binary or multiclass
    unique_labels = set(y_true + y_pred)
    is_binary = len(unique_labels) == 2
    
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='binary' if is_binary else 'weighted', zero_division=0),
        'recall': recall_score(y_true, y_pred, average='binary' if is_binary else 'weighted', zero_division=0),
        'f1': f1_score(y_true, y_pred, average='binary' if is_binary else 'weighted', zero_division=0),
    }
    
    # Add per-class metrics for multiclass
    if not is_binary:
        precision_per_class = precision_score(y_true, y_pred, average=None, labels=sorted(unique_labels), zero_division=0)
        recall_per_class = recall_score(y_true, y_pred, average=None, labels=sorted(unique_labels), zero_division=0)
        f1_per_class = f1_score(y_true, y_pred, average=None, labels=sorted(unique_labels), zero_division=0)
        
        metrics['per_class'] = {
            label: {
                'precision': float(precision_per_class[i]),
                'recall': float(recall_per_class[i]),
                'f1': float(f1_per_class[i])
            }
            for i, label in enumerate(sorted(unique_labels))
        }
    
    # Add confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=sorted(unique_labels))
    metrics['confusion_matrix'] = cm.tolist()
    
    return metrics