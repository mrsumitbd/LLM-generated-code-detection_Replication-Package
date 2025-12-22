def swizzle_2d(tile_id, num_pid_m, num_pid_n, GROUP_SIZE_M: tl.constexpr):
    return (tile_id // (num_pid_m * GROUP_SIZE_M) * num_pid_n * GROUP_SIZE_M +
            (tile_id % num_pid_m) * GROUP_SIZE_M +
            (tile_id // num_pid_m % GROUP_SIZE_M))