import pandas as pd
from typing import Any, Dict, float, str

def compute_default_metrics(
    samples_df: pd.DataFrame,
    answer_group_correctness_df: pd.DataFrame,
) -> dict[str, float | str | dict[Any, Any]]:
    """
    Compute standard metrics (pass, cons, etc.) for evals that can measure correctness at the level of answer groups (e.g., a multiple choice question for which one or more answers are correct).

    answer_group: an integer representing a group of answers that are considered equivalent. For example, all A answers
    for a given question.
    """
    # Group the samples_df by (instance, attempt, answer_group_id)
    grouped_samples = samples_df.groupby(["instance", "attempt", "answer_group_id"])

    # Compute the number of attempts per instance
    attempts_per_instance = grouped_samples.size().groupby("instance").count()

    # Compute the number of answer groups per instance
    answer_groups_per_instance = grouped_samples.size().groupby("instance").size()

    # Compute the number of correct answer groups per instance
    correct_answer_groups_per_instance = (
        answer_group_correctness_df[answer_group_correctness_df["is_correct"]]
        .groupby(["instance", "answer_group_id"])
        .size()
        .groupby("instance")
        .count()
    )

    # Compute the pass rate per instance
    pass_rate_per_instance = (
        correct_answer_groups_per_instance / answer_groups_per_instance
    )

    # Compute the consistency per instance
    consistency_per_instance = (
        correct_answer_groups_per_instance / attempts_per_instance
    )

    # Compute the overall metrics
    overall_metrics = {
        "pass_rate": pass_rate_per_instance.mean(),
        "consistency": consistency_per_instance.mean(),
        "pass_rate_per_instance": pass_rate_per_instance.to_dict(),
        "consistency_per_instance": consistency_per_instance.to_dict(),
    }

    return overall_metrics