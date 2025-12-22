def _quantize(x, bins):
    """
    Quantize the input array `x` into `bins` number of bins.
    
    Args:
        x (numpy.ndarray): Input array to be quantized.
        bins (int): Number of bins to quantize the input array into.
    
    Returns:
        numpy.ndarray: Quantized version of the input array `x`.
    """
    # Compute the minimum and maximum values of the input array
    x_min = x.min()
    x_max = x.max()
    
    # Compute the bin edges
    bin_edges = np.linspace(x_min, x_max, bins + 1)
    
    # Digitize the input array using the bin edges
    quantized = np.digitize(x, bin_edges[:-1])
    
    return quantized