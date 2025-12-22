import math

def gaussian_kernel_1d(sigma, truncate):
    """
    Create a 1D Gaussian kernel.
    
    Parameters:
    sigma: Standard deviation of the Gaussian kernel
    truncate: Truncate the kernel at this many standard deviations
    
    Returns:
    A 1D numpy array containing the Gaussian kernel
    """
    import numpy as np
    
    # Calculate the radius of the kernel
    radius = int(truncate * sigma + 0.5)
    
    # Create the kernel
    x = np.arange(-radius, radius + 1, dtype=np.float64)
    
    # Calculate the Gaussian values
    sigma_sq = sigma * sigma
    kernel = np.exp(-0.5 * x * x / sigma_sq)
    
    # Normalize the kernel so it sums to 1
    kernel = kernel / np.sum(kernel)
    
    return kernel