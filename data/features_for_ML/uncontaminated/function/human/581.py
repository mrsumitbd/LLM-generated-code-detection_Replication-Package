from typing import Any, Awaitable, Callable, Sequence, cast
import pandas as pd
from nanoeval.library_config import get_library_config

def compute_default_metrics(
    # (instance, attempt, answer_group_id [int])
    samples_df: pd.DataFrame,
    # (instance, answer_group_id [int], is_correct)
    answer_group_correctness_df: pd.DataFrame,
) -> dict[str, float | str | dict[Any, Any]]:
    """
    Compute standard metrics (pass, cons, etc.) for evals that can measure correctness at the level of answer groups (e.g., a multiple choice question for which one or more answers are correct).

    answer_group: an integer representing a group of answers that are considered equivalent. For example, all A answers
    for a given question.
    """

    _validate_input_data(samples_df, answer_group_correctness_df)

    return get_library_config().compute_default_metrics(samples_df, answer_group_correctness_df)