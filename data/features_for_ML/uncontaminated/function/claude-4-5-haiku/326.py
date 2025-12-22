def _quantize(x, bins):
    """Quantize a value x into one of the given bins."""
    if not bins:
        return x
    
    # Find the closest bin
    min_distance = float('inf')
    closest_bin = bins[0]
    
    for bin_val in bins:
        distance = abs(x - bin_val)
        if distance < min_distance:
            min_distance = distance
            closest_bin = bin_val
    
    return closest_bin