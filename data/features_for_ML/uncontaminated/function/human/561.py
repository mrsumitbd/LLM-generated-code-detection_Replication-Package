from typing import Dict, List
from .evaluate_factory import get_evaluator_from_gold_answer
import numpy as np

def calc_recall(pred: Dict, gold: Dict, use_gold_for_eval: bool):
    from .evaluate_factory import get_evaluator_from_gold_answer

    recall = []
    for gold_key, gold_value in gold.items():
        pred_value = pred.get(gold_key)
        gold_value = fix_number(gold_value)
        pred_value = fix_number(pred_value)
        if gold_key not in pred:
            recall.append(0)
        else:
            evaluator = (
                get_evaluator_from_gold_answer(type(gold_value))
                if use_gold_for_eval
                else get_evaluator_from_gold_answer(type(pred_value))
            )
            if not isinstance(pred_value, type(gold_value)):
                recall.append(0)
                continue
            recall.append(evaluator(pred_value, gold_value))
    avg_recall = np.average(recall)
    return avg_recall