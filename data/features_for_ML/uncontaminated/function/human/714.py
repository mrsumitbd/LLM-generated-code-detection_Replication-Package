import pandas as pd
from loguru import logger

def compute_annotator_metrics(
    votes_df: pd.DataFrame,
    annotator_metadata: dict,
    annotator_cols: list[str],
    ref_annotator_col: str,
) -> dict:

    # votes_df is a pd.DataFrame with one row
    # per vote, and columns "comparison_id", "principle", "vote"

    metric_dicts = get_metrics()

    # check that ref annotator col only contains "text_a" or "text_b"
    if not all(votes_df[ref_annotator_col].isin(["text_a", "text_b"])):
        values = ", ".join([str(v) for v in list(votes_df[ref_annotator_col].unique())])
        logger.warning(
            f"Reference annotator column '{ref_annotator_col}' contains values other than 'text_a' or 'text_b' (Values: {values}). Metrics will be computed on the subset of votes where the reference annotator is 'text_a' or 'text_b'."
        )
        votes_df = votes_df[
            votes_df[ref_annotator_col].isin(["text_a", "text_b"])
        ].copy()

    annotator_names = [
        annotator_metadata[col]["annotator_in_row_name"] for col in annotator_cols
    ]
    num_pairs = len(votes_df)

    metrics = {}

    for annotator_col in annotator_cols:

        annotator_name = annotator_metadata[annotator_col]["annotator_in_row_name"]

        votes_df = ensure_categories_identical(
            df=votes_df, col_a=annotator_col, col_b=ref_annotator_col
        )

        valid_votes_mask = votes_df[annotator_col].isin(["text_a", "text_b"])
        agree_mask = (
            votes_df[annotator_col] == votes_df[ref_annotator_col]
        ) & valid_votes_mask
        disagree_mask = valid_votes_mask & ~agree_mask

        annotation_a = votes_df[annotator_col].copy()
        annotation_b = votes_df[ref_annotator_col].copy()

        # make sure all annotations are strings
        annotation_a = annotation_a.astype(str)
        annotation_b = annotation_b.astype(str)

        # Initialize with "Not applicable" values
        agreement = pd.Series("Not applicable", index=votes_df.index)
        # Set values based on masks
        agreement[agree_mask] = "Agree"
        agreement[disagree_mask] = "Disagree"

        value_counts = agreement.value_counts(sort=False, dropna=False)
        value_counts = value_counts.fillna(0)

        for metric_name, metric_dict in metric_dicts.items():
            metric_fn = metric_dict["fn"]
            if metric_name not in metrics:
                metrics[metric_name] = {}
            metrics[metric_name][annotator_name] = metric_fn(
                value_counts, annotation_a=annotation_a, annotation_b=annotation_b
            )

    return {
        "annotator_names": annotator_names,
        "num_pairs": num_pairs,
        "metrics": metrics,
    }