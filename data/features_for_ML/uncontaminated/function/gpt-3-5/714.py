import pandas as pd

def compute_annotator_metrics(votes_df: pd.DataFrame, annotator_metadata: dict, annotator_cols: list[str], ref_annotator_col: str) -> dict:
    annotator_metrics = {}
    
    for annotator_col in annotator_cols:
        total_votes = votes_df.groupby(annotator_col).size()
        agreement_votes = votes_df[votes_df[annotator_col] == votes_df[ref_annotator_col]].groupby(annotator_col).size()
        
        annotator_metrics[annotator_col] = {
            'total_votes': total_votes.to_dict(),
            'agreement_votes': agreement_votes.to_dict(),
            'agreement_rate': agreement_votes.sum() / total_votes.sum()
        }
        
        if annotator_col in annotator_metadata:
            annotator_metrics[annotator_col]['metadata'] = annotator_metadata[annotator_col]
    
    return annotator_metrics