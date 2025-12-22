import numpy as np

def gaussian_kernel_1d(sigma, truncate):
    """
    Compute a 1D Gaussian kernel.

    Args:
        sigma (float): The standard deviation of the Gaussian kernel.
        truncate (float): The number of standard deviations at which to truncate the kernel.

    Returns:
        numpy.ndarray: The 1D Gaussian kernel.
    """
    x = np.arange(-truncate * sigma, truncate * sigma + 1)
    kernel = np.exp(-0.5 * (x / sigma) ** 2)
    return kernel / kernel.sum()