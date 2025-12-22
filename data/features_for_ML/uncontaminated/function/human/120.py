from loguru import logger

def _get_annotator_df_col_names(
    annotator_visible_names: list[str], votes_dicts: dict[str, dict]
) -> list[str]:
    """Get the column names of the annotators in votes_df from a list of visible names.

    Note that this fn can be used both for annotators shown in rows and columns of
    the final output plot. All annotators are columns in the original votes_df.

    This also gives warning if not all annotators are available across all datasets.
    """
    # get mappings from visible names to column names for each dataset
    visible_to_cols = {}
    for dataset_name, votes_dict in votes_dicts.items():
        metadata = votes_dict["annotator_metadata"]
        visible_to_col = {
            value["annotator_visible_name"]: col for col, value in metadata.items()
        }
        visible_to_cols[dataset_name] = visible_to_col

    updated_annotator_visible_names = []
    for annotator_name in annotator_visible_names:
        add_annotator = True
        for dataset_name, visible_to_col in visible_to_cols.items():
            if annotator_name not in visible_to_col:
                logger.warning(
                    f"Annotator '{annotator_name}' (visible name) not found in dataset '{dataset_name}'. Skipping this annotator. Available annotators in this dataset: {list(visible_to_col.keys())}"
                )
                add_annotator = False
        if add_annotator:
            updated_annotator_visible_names.append(annotator_name)

    # get column names for the remaining annotators
    col_names = [
        visible_to_col[annotator_name]
        for annotator_name in updated_annotator_visible_names
    ]
    return col_names