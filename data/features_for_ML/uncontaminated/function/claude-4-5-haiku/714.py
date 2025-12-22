def compute_annotator_metrics(
    votes_df: pd.DataFrame,
    annotator_metadata: dict,
    annotator_cols: list[str],
    ref_annotator_col: str,
) -> dict:
    """
    Compute annotator metrics including agreement with reference annotator.
    
    Args:
        votes_df: DataFrame with columns "comparison_id", "principle", "vote"
        annotator_metadata: Dictionary with annotator information
        annotator_cols: List of annotator column names
        ref_annotator_col: Reference annotator column name
        
    Returns:
        Dictionary with annotator metrics
    """
    metrics = {}
    
    # Get reference annotator votes
    if ref_annotator_col not in votes_df.columns:
        return metrics
    
    ref_votes = votes_df[ref_annotator_col]
    
    # Compute metrics for each annotator
    for annotator_col in annotator_cols:
        if annotator_col not in votes_df.columns:
            continue
            
        annotator_votes = votes_df[annotator_col]
        
        # Calculate agreement with reference
        valid_mask = ref_votes.notna() & annotator_votes.notna()
        
        if valid_mask.sum() == 0:
            metrics[annotator_col] = {
                "agreement": 0.0,
                "total_votes": 0,
                "matching_votes": 0
            }
            continue
        
        valid_ref = ref_votes[valid_mask]
        valid_annotator = annotator_votes[valid_mask]
        
        matching = (valid_ref == valid_annotator).sum()
        total = valid_mask.sum()
        agreement = matching / total if total > 0 else 0.0
        
        metrics[annotator_col] = {
            "agreement": agreement,
            "total_votes": int(total),
            "matching_votes": int(matching)
        }
    
    return metrics