def _get_default_annotator_cols_config(data) -> str:
    """Get the default annotator cols config.

    This sets the annotator columns to the default, and the rows to all principle annotators
    """
    annotator_cols = ['annotator_id', 'annotator_name', 'annotator_email']
    principle_annotators = data['annotators'].loc[data['annotators']['is_principle'] == True, 'annotator_id'].tolist()
    config = {
        'annotator_cols': annotator_cols,
        'annotator_rows': principle_annotators
    }
    return str(config)