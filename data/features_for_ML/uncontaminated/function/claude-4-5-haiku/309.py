def get_default_group_cast_config(num_ranks: int) -> "GrpCollConfig":
    """
    Get a recommended dispatch config.

    Argument:
        num_ranks: the number of ranks.

    Returns:
        config: the recommended config.
    """
    from torch.distributed.device_mesh import DeviceMesh
    from torch.distributed._tensor.api import GrpCollConfig
    
    # Determine the optimal configuration based on number of ranks
    if num_ranks <= 1:
        mesh_dim_names = ["rank"]
        mesh_shape = (num_ranks,)
    elif num_ranks <= 8:
        mesh_dim_names = ["rank"]
        mesh_shape = (num_ranks,)
    else:
        # For larger number of ranks, use a 2D mesh if possible
        import math
        sqrt_ranks = int(math.sqrt(num_ranks))
        if sqrt_ranks * sqrt_ranks == num_ranks:
            mesh_dim_names = ["row", "col"]
            mesh_shape = (sqrt_ranks, sqrt_ranks)
        else:
            mesh_dim_names = ["rank"]
            mesh_shape = (num_ranks,)
    
    # Create and return the default configuration
    return GrpCollConfig(
        mesh_dim_names=mesh_dim_names,
        mesh_shape=mesh_shape
    )