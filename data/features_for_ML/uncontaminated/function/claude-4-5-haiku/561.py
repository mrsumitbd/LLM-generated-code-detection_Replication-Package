def calc_recall(pred: Dict, gold: Dict, use_gold_for_eval: bool):
    """
    Calculate recall between predicted and gold standard dictionaries.
    
    Args:
        pred: Dictionary of predictions
        gold: Dictionary of gold standard values
        use_gold_for_eval: Whether to use gold standard for evaluation
    
    Returns:
        Recall score as a float between 0 and 1
    """
    if not gold:
        return 0.0
    
    if use_gold_for_eval:
        # Use gold standard as the reference set
        reference_set = set(gold.keys()) if isinstance(gold, dict) else set(gold)
    else:
        # Use predicted set as reference
        reference_set = set(pred.keys()) if isinstance(pred, dict) else set(pred)
    
    if not reference_set:
        return 0.0
    
    # Count true positives (items in both pred and gold)
    if isinstance(pred, dict) and isinstance(gold, dict):
        pred_set = set(pred.keys())
        gold_set = set(gold.keys())
    else:
        pred_set = set(pred) if not isinstance(pred, dict) else set(pred.keys())
        gold_set = set(gold) if not isinstance(gold, dict) else set(gold.keys())
    
    if use_gold_for_eval:
        # Recall = TP / (TP + FN) = correctly predicted / total gold
        true_positives = len(pred_set & gold_set)
        total_gold = len(gold_set)
        
        if total_gold == 0:
            return 0.0
        
        recall = true_positives / total_gold
    else:
        # Alternative recall calculation
        true_positives = len(pred_set & gold_set)
        total_pred = len(pred_set)
        
        if total_pred == 0:
            return 0.0
        
        recall = true_positives / total_pred
    
    return recall