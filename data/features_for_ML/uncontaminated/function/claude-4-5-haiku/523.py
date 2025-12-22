def mask_to_bias(mask: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
    """
    Convert a binary mask to an attention bias tensor.
    
    Args:
        mask: Binary mask tensor where 1 indicates valid positions and 0 indicates masked positions
        dtype: Data type for the output bias tensor
    
    Returns:
        Bias tensor where valid positions have 0 and masked positions have -inf
    """
    assert mask.dtype == torch.bool or mask.dtype == torch.uint8 or mask.dtype == torch.int64
    assert mask.dim() >= 2
    
    # Convert mask to float, then invert (0 -> 1, 1 -> 0)
    mask = mask.to(dtype=dtype)
    inverted_mask = 1.0 - mask
    
    # Convert to bias: valid positions (0) stay 0, masked positions (1) become -inf
    bias = inverted_mask.masked_fill(inverted_mask.to(torch.bool), torch.tensor(float('-inf'), dtype=dtype))
    
    return bias