def keep(conf):
    """
    Return a function that keeps only the specified keys from a dictionary.

    Parameters
    ----------
    conf : Iterable or Mapping
        If an iterable (list, set, tuple), it is interpreted as the set of keys to keep.
        If a mapping (dict), it is interpreted as a mapping from old keys to new keys.

    Returns
    -------
    function
        A function that takes a dictionary and returns a new dictionary containing
        only the specified keys (renamed if a mapping was provided).

    Raises
    ------
    TypeError
        If `conf` is not an iterable or mapping.
    """
    # Handle mapping (dict) first
    if isinstance(conf, dict):
        mapping = conf
        def _keep(d):
            return {mapping.get(k, k): v for k, v in d.items() if k in mapping}
        return _keep

    # Handle iterable of keys
    try:
        keys = set(conf)
    except TypeError:
        raise TypeError("keep expects an iterable of keys or a mapping")

    def _keep(d):
        return {k: d[k] for k in keys if k in d}

    return _keep