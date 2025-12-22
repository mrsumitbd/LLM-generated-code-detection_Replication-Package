import pandas as pd
from typing import Any, Dict

def compute_default_metrics(
    # (instance, attempt, answer_group_id [int])
    samples_df: pd.DataFrame,
    # (instance, answer_group_id [int], is_correct)
    answer_group_correctness_df: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Compute standard metrics (pass, consistency, accuracy, etc.) for evals that can measure correctness
    at the level of answer groups (e.g., a multiple choice question for which one or more answers are correct).

    Parameters
    ----------
    samples_df : pd.DataFrame
        DataFrame containing columns ['instance', 'attempt', 'answer_group_id'].
    answer_group_correctness_df : pd.DataFrame
        DataFrame containing columns ['instance', 'answer_group_id', 'is_correct'].

    Returns
    -------
    dict
        Dictionary with metrics:
            - 'pass_rate': proportion of instances with at least one correct answer group.
            - 'consistency_rate': proportion of instances where all attempts are either all correct or all incorrect.
            - 'accuracy': proportion of all attempts that are correct.
            - 'average_correctness_per_instance': average number of correct answer groups per instance.
    """
    # Ensure required columns exist
    required_samples = {"instance", "attempt", "answer_group_id"}
    required_correctness = {"instance", "answer_group_id", "is_correct"}
    if not required_samples.issubset(samples_df.columns):
        raise ValueError(f"samples_df must contain columns: {required_samples}")
    if not required_correctness.issubset(answer_group_correctness_df.columns):
        raise ValueError(f"answer_group_correctness_df must contain columns: {required_correctness}")

    # Merge to get correctness per attempt
    merged = pd.merge(
        samples_df,
        answer_group_correctness_df,
        on=["instance", "answer_group_id"],
        how="left",
    )

    # If some answer_group_id not found in correctness df, treat as incorrect
    merged["is_correct"] = merged["is_correct"].fillna(False).astype(bool)

    # Group by instance to compute per-instance metrics
    grouped = merged.groupby("instance")

    # Pass rate: at least one correct attempt per instance
    pass_series = grouped["is_correct"].any()
    pass_rate = pass_series.mean()

    # Consistency: all attempts same correctness per instance
    consistency_series = grouped["is_correct"].apply(lambda s: s.nunique() == 1)
    consistency_rate = consistency_series.mean()

    # Accuracy: overall proportion of correct attempts
    accuracy = merged["is_correct"].mean()

    # Average number of correct answer groups per instance
    correct_counts = grouped["is_correct"].sum()
    average_correctness_per_instance = correct_counts.mean()

    return {
        "pass_rate": float(pass_rate),
        "consistency_rate": float(consistency_rate),
        "accuracy": float(accuracy),
        "average_correctness_per_instance": float(average_correctness_per_instance),
    }