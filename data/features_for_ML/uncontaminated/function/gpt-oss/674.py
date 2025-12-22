import math
import numpy as np

def _compute_mean_and_conf_int(val):
    """
    Compute the mean and a 95% confidence interval for the given numeric values.

    Parameters
    ----------
    val : array-like
        Sequence of numeric values.

    Returns
    -------
    tuple
        (mean, lower_bound, upper_bound) where the bounds correspond to a
        95% confidence interval assuming a normal distribution.
    """
    # Convert to a NumPy array for convenience
    arr = np.asarray(val, dtype=float)

    # Handle empty input
    if arr.size == 0:
        return (float('nan'), float('nan'), float('nan'))

    # Compute mean
    mean = np.mean(arr)

    # Compute standard deviation (sample, ddof=1)
    if arr.size > 1:
        std = np.std(arr, ddof=1)
    else:
        std = 0.0

    # Standard error
    se = std / math.sqrt(arr.size)

    # 95% confidence interval using z-score 1.96
    z = 1.96
    lower = mean - z * se
    upper = mean + z * se

    return (mean, lower, upper)