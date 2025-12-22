import pandas as pd

def compute_annotator_metrics(
    votes_df: pd.DataFrame,
    annotator_metadata: dict,
    annotator_cols: list[str],
    ref_annotator_col: str,
) -> dict:
    metrics = {}
    for annotator_col in annotator_cols:
        annotator_name = annotator_metadata[annotator_col]['name']
        annotator_votes = votes_df[['comparison_id', 'principle', annotator_col, ref_annotator_col]]
        annotator_votes = annotator_votes.dropna(subset=[annotator_col, ref_annotator_col])

        agreement_count = (
            annotator_votes[annotator_col] == annotator_votes[ref_annotator_col]
        ).sum()
        total_count = len(annotator_votes)
        agreement_rate = agreement_count / total_count

        metrics[annotator_name] = {
            'agreement_count': agreement_count,
            'total_count': total_count,
            'agreement_rate': agreement_rate,
        }

    return metrics