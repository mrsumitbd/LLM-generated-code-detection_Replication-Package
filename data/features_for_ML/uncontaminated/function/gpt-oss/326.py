import numpy as np

def _quantize(x, bins):
    """
    Quantize the input values `x` into discrete bins.

    Parameters
    ----------
    x : array_like
        Input values to be quantized.
    bins : int or array_like
        If an integer, it specifies the number of equal-width bins
        spanning the range of `x`. If array-like, it must contain
        monotonically increasing bin edges (length = n_bins + 1).

    Returns
    -------
    indices : ndarray
        Integer indices of the bin each element of `x` falls into.
        The indices are 0-based and range from 0 to n_bins-1.
    """
    x_arr = np.asarray(x)

    # Determine bin edges
    if np.isscalar(bins):
        # Create equal-width bins over the range of x
        if x_arr.size == 0:
            # No data: return empty array of appropriate shape
            return np.empty_like(x_arr, dtype=int)
        min_val, max_val = np.min(x_arr), np.max(x_arr)
        # If all values are identical, create a single bin
        if min_val == max_val:
            bin_edges = np.array([min_val, max_val + 1.0])
        else:
            bin_edges = np.linspace(min_val, max_val, bins + 1)
    else:
        bin_edges = np.asarray(bins)
        if bin_edges.ndim != 1:
            raise ValueError("bins must be a 1-D array of bin edges")
        if bin_edges.size < 2:
            raise ValueError("bins must contain at least two edges")
        if not np.all(np.diff(bin_edges) >= 0):
            raise ValueError("bins must be monotonically increasing")

    # Use numpy.digitize to find bin indices
    # digitize returns indices in [1, len(bin_edges)] for each element
    # Subtract 1 to get 0-based indices
    indices = np.digitize(x_arr, bin_edges, right=False) - 1

    # Clip indices to valid range [0, n_bins-1]
    n_bins = len(bin_edges) - 1
    indices = np.clip(indices, 0, n_bins - 1)

    return indices