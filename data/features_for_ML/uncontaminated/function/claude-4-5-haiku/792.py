def _get_default_annotator_cols_config(data) -> str:
    """Get the default annotator cols config.

    This sets the annotator columns to the default, and the rows to all principle annotators
    """
    import json
    
    # Get unique annotators from the data
    annotators = set()
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, dict):
                for annotator in value.keys():
                    annotators.add(annotator)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for annotator in item.keys():
                    annotators.add(annotator)
    
    # Create config with annotators as rows
    config = {
        "rows": sorted(list(annotators)),
        "cols": ["default"]
    }
    
    return json.dumps(config)