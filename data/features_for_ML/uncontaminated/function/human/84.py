from typing import Dict, List
from .utils import _align_bags
import numpy as np

def evaluate_dicts(pred: List[Dict], gold: List[Dict]):
    if not (
        isinstance(pred, dict)
        or len(pred) == 0
        or (isinstance(pred, list) and isinstance(pred[0], dict))
    ):
        return 0
    max_alignment_scores = _align_bags(pred, gold, evaluate_pair_of_dicts)
    return np.average(max_alignment_scores)