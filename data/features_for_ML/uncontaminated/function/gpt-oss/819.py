def swizzle_2d(tile_id, num_pid_m, num_pid_n, GROUP_SIZE_M: tl.constexpr):
    """
    Compute the 2‑D process‑grid coordinates (pid_m, pid_n) from a linear tile index.
    The tile index is assumed to be laid out row‑major over the process grid:
        tile_id = pid_m * num_pid_n + pid_n
    The GROUP_SIZE_M parameter is accepted for API compatibility but is not used
    in this simple implementation.
    """
    pid_m = tile_id // num_pid_n
    pid_n = tile_id % num_pid_n
    return pid_m, pid_n