def get_default_group_cast_config(num_ranks: int) -> "GrpCollConfig":
    if num_ranks <= 4:
        return GrpCollConfig(1, 1, 1)
    elif num_ranks <= 16:
        return GrpCollConfig(2, 2, 2)
    elif num_ranks <= 64:
        return GrpCollConfig(4, 4, 4)
    else:
        return GrpCollConfig(8, 8, 8)