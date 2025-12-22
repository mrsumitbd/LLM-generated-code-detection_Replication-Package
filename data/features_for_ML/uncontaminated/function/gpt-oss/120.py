def _get_annotator_df_col_names(
    annotator_visible_names: list[str], votes_dicts: dict[str, dict]
) -> list[str]:
    """Get the column names of the annotators in votes_df from a list of visible names.

    Note that this fn can be used both for annotators shown in rows and columns of
    the final output plot. All annotators are columns in the original votes_df.

    This also gives warning if not all annotators are available across all datasets.
    """
    import warnings

    # Collect all annotator names that appear in any dataset
    all_annotators = set()
    for dataset_name, annotator_dict in votes_dicts.items():
        if not isinstance(annotator_dict, dict):
            continue
        all_annotators.update(annotator_dict.keys())

    # Determine which visible names are actually present
    present_names = [name for name in annotator_visible_names if name in all_annotators]

    # Warn about names that are not present in any dataset
    missing_names = [name for name in annotator_visible_names if name not in all_annotators]
    for name in missing_names:
        warnings.warn(
            f"Annotator '{name}' not found in any dataset; it will be omitted from the plot.",
            RuntimeWarning,
        )

    # Warn about names that are missing in some datasets
    for name in present_names:
        missing_in = [ds for ds, adict in votes_dicts.items() if name not in adict]
        if missing_in:
            warnings.warn(
                f"Annotator '{name}' is missing in datasets: {', '.join(missing_in)}; "
                "it will still be included but may have missing values.",
                RuntimeWarning,
            )

    return present_names