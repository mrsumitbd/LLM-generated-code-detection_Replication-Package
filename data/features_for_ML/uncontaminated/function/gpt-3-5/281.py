from typing import List, Optional, Dict

def evaluate_exact(
        ground_truth_calls: List[ToolCall],
        prediction_calls: List[ToolCall],
        task_id: Optional[str] = None,
        weights: Optional[Dict[str, float]] = None,
        thresholds: Optional[Dict[str, float]] = None,
    ) -> ToolEvalResult:
    
    return evaluate_task(ground_truth_calls, prediction_calls, match_type="strict", task_id=task_id, weights=weights, thresholds=thresholds)