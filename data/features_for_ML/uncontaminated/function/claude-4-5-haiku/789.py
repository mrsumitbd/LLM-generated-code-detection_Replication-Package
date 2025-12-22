def _compute_statistics(self, x, m, dim=2, eps=1e-5):
    """Compute mean and variance statistics for normalization."""
    # Compute mean along the specified dimension
    mean = x.mean(dim=dim, keepdim=True)
    
    # Compute variance along the specified dimension
    var = x.var(dim=dim, keepdim=True, unbiased=False)
    
    # Normalize
    x_normalized = (x - mean) / (var + eps).sqrt()
    
    return x_normalized, mean, var