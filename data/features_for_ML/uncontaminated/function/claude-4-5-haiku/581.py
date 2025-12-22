def compute_default_metrics(
    samples_df: pd.DataFrame,
    answer_group_correctness_df: pd.DataFrame,
) -> dict[str, float | str | dict[Any, Any]]:
    """
    Compute standard metrics (pass, cons, etc.) for evals that can measure correctness at the level of answer groups (e.g., a multiple choice question for which one or more answers are correct).

    answer_group: an integer representing a group of answers that are considered equivalent. For example, all A answers
    for a given question.
    """
    # Merge samples with answer group correctness
    merged_df = samples_df.merge(
        answer_group_correctness_df,
        on=["instance", "answer_group_id"],
        how="left"
    )
    
    # Get the correct answer for each instance (should be consistent within instance)
    instance_correctness = merged_df.groupby("instance")["is_correct"].first()
    
    # Calculate pass rate (fraction of instances where the answer was correct)
    total_instances = len(instance_correctness)
    if total_instances == 0:
        pass_rate = 0.0
    else:
        pass_rate = instance_correctness.sum() / total_instances
    
    # Calculate consistency (fraction of attempts that match the first attempt for each instance)
    consistency_scores = []
    for instance in merged_df["instance"].unique():
        instance_data = merged_df[merged_df["instance"] == instance]
        if len(instance_data) > 0:
            first_answer_group = instance_data["answer_group_id"].iloc[0]
            matching_attempts = (instance_data["answer_group_id"] == first_answer_group).sum()
            consistency = matching_attempts / len(instance_data)
            consistency_scores.append(consistency)
    
    consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.0
    
    # Build metrics dictionary
    metrics = {
        "pass": pass_rate,
        "cons": consistency,
    }
    
    return metrics