import numpy as np

def gaussian_kernel_1d(sigma, truncate):
    radius = int(truncate * sigma + 0.5)
    size = 2 * radius + 1
    kernel = np.empty(size, dtype=np.float64)
    sum_val = 0.0
    for i in range(size):
        x = i - radius
        val = np.exp(-0.5 * (x / sigma) ** 2)
        kernel[i] = val
        sum_val += val
    for i in range(size):
        kernel[i] /= sum_val
    return kernel, radius