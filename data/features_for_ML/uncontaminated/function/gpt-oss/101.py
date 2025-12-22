def _split_args_kwargs_data_proto(chunks, *args, **kwargs):
    """
    Split positional and keyword arguments into two dictionaries:
    - `data`: mapping of chunk names to values (positional args first, then keyword overrides)
    - `proto`: remaining keyword arguments that are not part of `chunks`

    Parameters
    ----------
    chunks : iterable
        An iterable of keys that represent the expected positional arguments.
    *args : tuple
        Positional values corresponding to the keys in `chunks`.
    **kwargs : dict
        Keyword arguments that may include values for the keys in `chunks`
        or other keys that should be returned in `proto`.

    Returns
    -------
    tuple
        A tuple `(data, proto)` where `data` is a dict mapping chunk names
        to their values, and `proto` is a dict of the remaining keyword
        arguments.
    """
    # Ensure chunks is a list for repeated indexing
    chunk_list = list(chunks)

    # Build the data dictionary from positional args
    data = {}
    for i, key in enumerate(chunk_list):
        if i < len(args):
            data[key] = args[i]
        elif key in kwargs:
            # Keyword override for missing positional arg
            data[key] = kwargs.pop(key)
        else:
            # No value provided; default to None
            data[key] = None

    # Remaining kwargs are considered proto arguments
    proto = kwargs

    return data, proto