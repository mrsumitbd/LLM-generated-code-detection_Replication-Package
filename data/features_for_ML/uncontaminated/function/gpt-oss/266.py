import numpy as np

def dtw_cuda(x, BLOCK_SIZE=1024):
    """
    Compute the Dynamic Time Warping (DTW) distance between two sequences
    represented by a cost matrix `x`. This implementation is a CPU fallback
    that mimics the structure of a CUDA-accelerated version.

    Parameters
    ----------
    x : np.ndarray
        2-D array of shape (N, M) containing the pairwise cost between
        elements of two sequences. The element x[i, j] should represent
        the cost of aligning element i of the first sequence with element j
        of the second sequence.
    BLOCK_SIZE : int, optional
        Block size parameter for CUDA kernels (ignored in this CPU
        implementation). Included for API compatibility.

    Returns
    -------
    float
        The DTW distance between the two sequences, i.e. the accumulated
        cost at the bottom-right corner of the cost matrix.
    """
    # Ensure input is a NumPy array of float type
    x = np.asarray(x, dtype=np.float64)

    if x.ndim != 2:
        raise ValueError("Input cost matrix `x` must be 2-dimensional")

    n, m = x.shape
    # Allocate the accumulated cost matrix
    acc = np.empty((n, m), dtype=np.float64)

    # Initialize the first cell
    acc[0, 0] = x[0, 0]

    # Initialize first row (only right moves)
    for j in range(1, m):
        acc[0, j] = acc[0, j - 1] + x[0, j]

    # Initialize first column (only down moves)
    for i in range(1, n):
        acc[i, 0] = acc[i - 1, 0] + x[i, 0]

    # Fill the rest of the matrix
    for i in range(1, n):
        # Local references for speed
        acc_i = acc[i]
        acc_im1 = acc[i - 1]
        x_i = x[i]
        for j in range(1, m):
            # Minimum of the three possible predecessors
            prev_min = min(acc_im1[j],     # diagonal
                           acc_i[j - 1],   # left
                           acc_im1[j - 1]) # up-left
            acc_i[j] = x_i[j] + prev_min

    # The DTW distance is the accumulated cost at the bottom-right corner
    return acc[-1, -1]