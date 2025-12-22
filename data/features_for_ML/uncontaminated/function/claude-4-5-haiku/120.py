def _get_annotator_df_col_names(
    annotator_visible_names: list[str], votes_dicts: dict[str, dict]
) -> list[str]:
    """Get the column names of the annotators in votes_df from a list of visible names.

    Note that this fn can be used both for annotators shown in rows and columns of
    the final output plot. All annotators are columns in the original votes_df.

    This also gives warning if not all annotators are available across all datasets.
    """
    import warnings
    
    # Collect all available annotators across all datasets
    all_annotators = set()
    for dataset_votes in votes_dicts.values():
        all_annotators.update(dataset_votes.keys())
    
    # Map visible names to actual column names
    result = []
    missing_annotators = []
    
    for visible_name in annotator_visible_names:
        # Check if visible_name is directly in all_annotators
        if visible_name in all_annotators:
            result.append(visible_name)
        else:
            # Try to find a match (could be an alias or different format)
            found = False
            for annotator in all_annotators:
                if annotator == visible_name or str(annotator) == visible_name:
                    result.append(annotator)
                    found = True
                    break
            
            if not found:
                missing_annotators.append(visible_name)
    
    # Check if all annotators are available across all datasets
    for annotator in result:
        datasets_with_annotator = sum(
            1 for dataset_votes in votes_dicts.values() 
            if annotator in dataset_votes
        )
        if datasets_with_annotator < len(votes_dicts):
            warnings.warn(
                f"Annotator '{annotator}' is not available in all datasets. "
                f"Available in {datasets_with_annotator}/{len(votes_dicts)} datasets.",
                UserWarning
            )
    
    if missing_annotators:
        warnings.warn(
            f"The following annotators were not found: {missing_annotators}",
            UserWarning
        )
    
    return result