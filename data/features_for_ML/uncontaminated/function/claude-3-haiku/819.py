import numpy as np

def swizzle_2d(tile_id, num_pid_m, num_pid_n, GROUP_SIZE_M: tl.constexpr):
    """
    Swizzle a 2D tile index to a 1D index.

    Args:
        tile_id (int): The 2D tile index.
        num_pid_m (int): The number of tiles in the M dimension.
        num_pid_n (int): The number of tiles in the N dimension.
        GROUP_SIZE_M (int): The group size in the M dimension.

    Returns:
        int: The 1D index of the tile.
    """
    tile_m = tile_id // num_pid_n
    tile_n = tile_id % num_pid_n

    group_m = tile_m // GROUP_SIZE_M
    group_n = tile_n // GROUP_SIZE_M

    local_m = tile_m % GROUP_SIZE_M
    local_n = tile_n % GROUP_SIZE_M

    return (group_m * (num_pid_n // GROUP_SIZE_M) * GROUP_SIZE_M * GROUP_SIZE_M +
            group_n * GROUP_SIZE_M * GROUP_SIZE_M +
            local_m * GROUP_SIZE_M +
            local_n)