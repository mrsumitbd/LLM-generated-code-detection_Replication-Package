def get_default_group_cast_config(num_ranks: int) -> "GrpCollConfig":
    """
    Get a recommended dispatch config.

    Argument:
        num_ranks: the number of ranks.

    Returns:
        config: the recommended config.
    """
    if num_ranks <= 4:
        return GrpCollConfig(
            group_size=num_ranks,
            num_chunks=1,
            chunk_size=num_ranks,
            use_hierarchical_broadcast=False,
            use_hierarchical_reduce=False,
        )
    elif num_ranks <= 8:
        return GrpCollConfig(
            group_size=4,
            num_chunks=2,
            chunk_size=2,
            use_hierarchical_broadcast=True,
            use_hierarchical_reduce=True,
        )
    else:
        return GrpCollConfig(
            group_size=4,
            num_chunks=num_ranks // 4,
            chunk_size=4,
            use_hierarchical_broadcast=True,
            use_hierarchical_reduce=True,
        )