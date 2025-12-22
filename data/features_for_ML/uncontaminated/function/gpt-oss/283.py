def diamond_peptidase_options(func):
    """
    Decorator that injects default Diamond options into the wrapped function.
    The wrapped function must accept an `options` keyword argument.
    """
    def wrapper(*args, **kwargs):
        # Extract user-provided options if any
        user_opts = kwargs.pop("options", {})
        # Default options for Diamond peptidase searches
        default_opts = {
            "evalue": 1e-5,
            "max_target_seqs": 1,
            "threads": 1,
            "matrix": "BLOSUM62",
            "gapopen": 11,
            "gapextend": 1,
            "filter": "no",
            "subject": None,
            "query": None,
            "outfmt": 6,
        }
        # Merge defaults with user options (user overrides defaults)
        merged_opts = {**default_opts, **user_opts}
        # Pass the merged options back to the function
        kwargs["options"] = merged_opts
        return func(*args, **kwargs)
    return wrapper