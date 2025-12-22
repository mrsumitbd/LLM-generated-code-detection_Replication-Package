def _get_annotator_df_col_names(annotator_visible_names: list[str], votes_dicts: dict[str, dict]) -> list[str]:
    annotator_col_names = []
    for annotator_name in annotator_visible_names:
        if annotator_name in votes_dicts:
            annotator_col_names.extend(votes_dicts[annotator_name].keys())
        else:
            print(f"Warning: Annotator '{annotator_name}' not available in all datasets.")
    return annotator_col_names