import pandas as pd
from typing import List, Dict, Any

def compute_annotator_metrics(
    votes_df: pd.DataFrame,
    annotator_metadata: Dict[str, Any],
    annotator_cols: List[str],
    ref_annotator_col: str,
) -> Dict[str, Dict[str, float]]:
    """
    Compute accuracy, precision, recall and F1 score for each annotator in
    `annotator_cols` relative to the reference annotator specified by
    `ref_annotator_col`.

    Parameters
    ----------
    votes_df : pd.DataFrame
        DataFrame with one row per comparison. Expected columns:
        - "comparison_id"
        - "principle"
        - "vote" : a mapping (dict) from annotator name to vote value
    annotator_metadata : dict
        Mapping from annotator name to arbitrary metadata. Not used in
        the current implementation but kept for API compatibility.
    annotator_cols : list[str]
        List of annotator names for which metrics should be computed.
    ref_annotator_col : str
        Name of the reference annotator in the vote mapping.

    Returns
    -------
    dict
        Mapping from annotator name to a dict of metrics:
        {"accuracy": float, "precision": float, "recall": float, "f1": float}
    """
    # Ensure the vote column contains mappings
    if not isinstance(votes_df.dtypes.get("vote"), pd.core.dtypes.dtypes.ObjectDtype):
        raise ValueError("The 'vote' column must contain mapping objects (dicts).")

    # Prepare result dictionary
    results: Dict[str, Dict[str, float]] = {}

    # Iterate over each annotator to compute metrics
    for annotator in annotator_cols:
        # Extract votes for the annotator and reference annotator
        annotator_votes = []
        ref_votes = []

        for _, row in votes_df.iterrows():
            vote_map = row["vote"]
            # Skip rows where either annotator or reference is missing
            if annotator not in vote_map or ref_annotator_col not in vote_map:
                continue
            annotator_votes.append(vote_map[annotator])
            ref_votes.append(vote_map[ref_annotator_col])

        # If no votes are available, skip this annotator
        if not annotator_votes:
            continue

        # Convert to lists of integers (assuming binary classification 0/1)
        try:
            y_true = [int(v) for v in ref_votes]
            y_pred = [int(v) for v in annotator_votes]
        except Exception:
            # If conversion fails, skip this annotator
            continue

        # Compute confusion matrix components
        tp = sum((p == 1 and t == 1) for p, t in zip(y_pred, y_true))
        fp = sum((p == 1 and t == 0) for p, t in zip(y_pred, y_true))
        fn = sum((p == 0 and t == 1) for p, t in zip(y_pred, y_true))
        tn = sum((p == 0 and t == 0) for p, t in zip(y_pred, y_true))

        # Accuracy
        accuracy = (tp + tn) / len(y_true) if y_true else 0.0

        # Precision
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0

        # Recall
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        # F1 score
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        results[annotator] = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    return results