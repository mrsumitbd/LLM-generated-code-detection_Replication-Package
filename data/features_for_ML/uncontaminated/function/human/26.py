from typing import Any, Dict, List, Tuple, cast
from verifiers.types import GenerateOutputs, Messages

def compute_summary(results: GenerateOutputs) -> Dict[str, Any]:
    """Compute aggregated statistics from GenerateOutputs in a format usable by templates.

    This function intentionally does not change layout based on dataset size.
    """
    summary: Dict[str, Any] = {}

    reward_stats = _compute_basic_stats(results.reward)
    reward_percentiles = _compute_percentiles(results.reward)
    summary["reward"] = {**reward_stats, **reward_percentiles}

    metric_summaries: Dict[str, Dict[str, float]] = {}
    for metric_name, metric_values in results.metrics.items():
        metric_summaries[metric_name] = {
            **_compute_basic_stats(metric_values),
            **_compute_percentiles(metric_values),
        }
    summary["metrics"] = metric_summaries

    return summary