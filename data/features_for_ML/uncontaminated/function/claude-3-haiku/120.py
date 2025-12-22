def _get_annotator_df_col_names(
    annotator_visible_names: list[str], votes_dicts: dict[str, dict]
) -> list[str]:
    """Get the column names of the annotators in votes_df from a list of visible names.

    Note that this fn can be used both for annotators shown in rows and columns of
    the final output plot. All annotators are columns in the original votes_df.

    This also gives warning if not all annotators are available across all datasets.
    """
    all_annotators = set()
    for vote_dict in votes_dicts.values():
        all_annotators.update(vote_dict.keys())

    annotator_df_col_names = []
    for visible_name in annotator_visible_names:
        if visible_name in all_annotators:
            annotator_df_col_names.append(visible_name)
        else:
            print(f"Warning: Annotator '{visible_name}' not found in all datasets.")

    return annotator_df_col_names