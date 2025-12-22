def _get_default_annotator_cols_config(data) -> str:
    """
    Get the default annotator cols config.

    This sets the annotator columns to the default, and the rows to all principle annotators.
    The function accepts several common data structures that may contain annotator information:
        * pandas.DataFrame with columns 'annotator' and 'principal'
        * dict mapping annotator names to a dict that contains a 'principal' key
        * list of dicts each containing 'annotator' and 'principal'
        * list of tuples (annotator, principal)
    The returned string is formatted as:
        "default:<comma‑separated list of principal annotator names>"
    If no principal annotators are found, the string will be "default:".
    """
    principals = []

    # Handle pandas DataFrame if available
    try:
        import pandas as pd
        if isinstance(data, pd.DataFrame):
            if 'annotator' in data.columns and 'principal' in data.columns:
                principals = data.loc[data['principal'], 'annotator'].astype(str).tolist()
    except Exception:
        pass

    # Handle dict mapping annotator -> dict with 'principal'
    if not principals and isinstance(data, dict):
        for name, info in data.items():
            if isinstance(info, dict) and info.get('principal'):
                principals.append(str(name))

    # Handle list of dicts
    if not principals and isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if item.get('principal') and 'annotator' in item:
                    principals.append(str(item['annotator']))
            elif isinstance(item, (tuple, list)) and len(item) == 2:
                annotator, principal = item
                if principal:
                    principals.append(str(annotator))

    # Ensure unique and sorted for consistency
    principals = sorted(set(principals))

    return f"default:{','.join(principals)}"