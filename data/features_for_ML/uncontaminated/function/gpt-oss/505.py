def kernel_inter_node_p2p_for_same_local_rank(offset, local_world_size, M_per_rank, N,
                                              input,  # [M, N]
                                              output,  # [M, N]
                                              ):
    """
    Copy the block of rows belonging to the current local rank from `input` to
    the corresponding block in `output`.  The `offset` argument specifies the
    local rank index (0‑based).  Each rank owns `M_per_rank` consecutive rows.
    The function assumes that `input` contains the data for the current rank
    only (i.e. the first `M_per_rank` rows).  The destination block in
    `output` is located at rows `offset * M_per_rank` to
    `(offset + 1) * M_per_rank - 1`.

    Parameters
    ----------
    offset : int
        Local rank index (0‑based).
    local_world_size : int
        Total number of local ranks (unused in this implementation but kept
        for API compatibility).
    M_per_rank : int
        Number of rows owned by each rank.
    N : int
        Number of columns.
    input : np.ndarray
        Source array of shape (M, N).  Only the first `M_per_rank` rows are
        used.
    output : np.ndarray
        Destination array of shape (M, N).  The block corresponding to the
        current rank will be overwritten.

    Notes
    -----
    This implementation is intentionally simple and does not perform any
    communication; it merely copies data within a single process.  It is
    suitable for unit testing or as a placeholder for a more complex
    inter‑node communication kernel.
    """
    import numpy as np

    # Validate shapes
    if input.ndim != 2 or output.ndim != 2:
        raise ValueError("input and output must be 2‑D arrays")
    if input.shape[1] != N or output.shape[1] != N:
        raise ValueError("column dimension mismatch")
    if input.shape[0] < M_per_rank:
        raise ValueError("input does not contain enough rows for M_per_rank")
    if output.shape[0] < (offset + 1) * M_per_rank:
        raise ValueError("output does not have enough rows for the target block")

    # Compute destination slice
    dst_start = offset * M_per_rank
    dst_end = dst_start + M_per_rank

    # Perform the copy
    output[dst_start:dst_end, :] = input[:M_per_rank, :]

    # Return nothing (in‑place operation)
    return