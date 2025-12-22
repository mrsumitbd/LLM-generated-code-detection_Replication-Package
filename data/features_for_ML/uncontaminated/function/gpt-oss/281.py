from typing import List, Optional, Dict

# Assume these are defined elsewhere in the same package
from .types import ToolCall, ToolEvalResult
from .evaluation import evaluate_task


def evaluate_exact(
    ground_truth_calls: List[ToolCall],
    prediction_calls: List[ToolCall],
    task_id: Optional[str] = None,
    weights: Optional[Dict[str, float]] = None,
    thresholds: Optional[Dict[str, float]] = None,
) -> ToolEvalResult:
    """
    Evaluate tool calls using strict/exact matching criteria.
    This is a convenience method that calls evaluate_task with match_type="strict".

    Args:
        ground_truth_calls: List of expected tool calls
        prediction_calls: List of actual tool calls made by the model
        task_id: Optional identifier for the task
        weights: Optional dictionary with custom weights
        thresholds: Optional dictionary with custom thresholds

    Returns:
        ToolEvalResult with strict evaluation metrics
    """
    return evaluate_task(
        ground_truth_calls=ground_truth_calls,
        prediction_calls=prediction_calls,
        task_id=task_id,
        weights=weights,
        thresholds=thresholds,
        match_type="strict",
    )