import numpy as np

def gaussian_kernel_1d(sigma, truncate):
    size = int(truncate * sigma + 0.5)
    x = np.arange(-size, size + 1)
    kernel = np.exp(-x**2 / (2 * sigma**2))
    kernel /= np.sum(kernel)
    return kernel