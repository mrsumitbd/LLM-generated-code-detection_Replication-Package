import pandas as pd
from typing import Any

def compute_default_metrics(
    samples_df: pd.DataFrame,
    answer_group_correctness_df: pd.DataFrame,
) -> dict[str, float | str | dict[Any, Any]]:
    
    metrics = {}
    
    pass_rate = answer_group_correctness_df['is_correct'].mean()
    metrics['pass'] = pass_rate
    
    correct_count = answer_group_correctness_df[answer_group_correctness_df['is_correct'] == True].shape[0]
    total_count = answer_group_correctness_df.shape[0]
    metrics['cons'] = correct_count / total_count if total_count > 0 else 'N/A'
    
    metrics['samples'] = samples_df.shape[0]
    
    return metrics