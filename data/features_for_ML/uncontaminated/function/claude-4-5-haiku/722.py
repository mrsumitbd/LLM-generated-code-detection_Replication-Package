def log_norm(x, mean=-4, std=4, dim=2):
    """
    normalized log mel -> mel -> norm -> log(norm)
    """
    import torch
    
    # Denormalize: reverse the normalization
    x = x * std + mean
    
    # Convert from log scale back to linear scale
    x = torch.exp(x)
    
    # Compute norm along the specified dimension
    x = torch.norm(x, dim=dim, keepdim=True)
    
    # Convert back to log scale
    x = torch.log(x)
    
    return x