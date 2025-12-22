import numpy as np

def gaussian_kernel_1d(sigma, truncate):
    """
    Generate a 1‑D Gaussian kernel.

    Parameters
    ----------
    sigma : float
        Standard deviation of the Gaussian.
    truncate : float
        Truncate the filter at this many standard deviations.

    Returns
    -------
    kernel : np.ndarray
        1‑D array of kernel weights, normalized to sum to 1.
    """
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    # Determine kernel radius
    radius = int(np.ceil(truncate * sigma))
    # Create coordinate array
    x = np.arange(-radius, radius + 1, dtype=np.float64)
    # Compute Gaussian values
    kernel = np.exp(-(x ** 2) / (2 * sigma ** 2))
    # Normalize
    kernel /= kernel.sum()
    return kernel