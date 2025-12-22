def swizzle_2d(tile_id, num_pid_m, num_pid_n, GROUP_SIZE_M: tl.constexpr):
    """
    Swizzle 2D tile IDs to improve cache locality.
    Maps a linear tile_id to a 2D (pid_m, pid_n) coordinate with swizzling.
    """
    # Calculate the number of groups in M dimension
    num_groups_m = tl.cdiv(num_pid_m, GROUP_SIZE_M)
    
    # Swizzle by grouping tiles in M dimension
    # First, determine which group this tile belongs to
    group_id = tile_id // (GROUP_SIZE_M * num_pid_n)
    
    # Position within the group
    pos_in_group = tile_id % (GROUP_SIZE_M * num_pid_n)
    
    # Extract pid_n and local pid_m from position in group
    pid_n = pos_in_group // GROUP_SIZE_M
    pid_m_local = pos_in_group % GROUP_SIZE_M
    
    # Calculate actual pid_m
    pid_m = group_id * GROUP_SIZE_M + pid_m_local
    
    return pid_m, pid_n