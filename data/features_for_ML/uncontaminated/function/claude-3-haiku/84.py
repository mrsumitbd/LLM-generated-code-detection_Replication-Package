from typing import List, Dict

def evaluate_dicts(pred: List[Dict], gold: List[Dict]):
    """
    Evaluates the performance of a model by comparing the predicted dictionaries (pred) with the ground truth dictionaries (gold).
    
    Args:
        pred (List[Dict]): A list of predicted dictionaries.
        gold (List[Dict]): A list of ground truth dictionaries.
    
    Returns:
        A dictionary containing the evaluation metrics.
    """
    if len(pred) != len(gold):
        raise ValueError("The lengths of the predicted and ground truth lists must be equal.")
    
    correct = 0
    total = len(pred)
    
    for p, g in zip(pred, gold):
        if p == g:
            correct += 1
    
    accuracy = correct / total
    
    return {"accuracy": accuracy}