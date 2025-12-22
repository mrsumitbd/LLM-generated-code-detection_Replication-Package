def run_roomie_diagnostics(old, new):
    """
    Run diagnostics comparing two roomie data dictionaries.

    Parameters
    ----------
    old : dict
        The original roomie data.
    new : dict
        The updated roomie data.

    Returns
    -------
    dict or None
        A dictionary mapping keys that changed to a dict containing the old and new values.
        If the new data is in edit mode (i.e., new.get('edit_mode') is truthy), diagnostics are not run and None is returned.
    """
    # Do not run diagnostics in edit mode
    if new.get('edit_mode'):
        return None

    diagnostics = {}
    # Compare all keys present in either dictionary
    all_keys = set(old.keys()).union(new.keys())
    for key in all_keys:
        old_val = old.get(key)
        new_val = new.get(key)
        if old_val != new_val:
            diagnostics[key] = {'old': old_val, 'new': new_val}

    return diagnostics