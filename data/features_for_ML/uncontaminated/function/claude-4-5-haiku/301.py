def mean_with_nan(input, dim=None, keepdim=False):
    """
    Mean of a tensor. Ignore all nan values.

    Parameters:
        input (Tensor): input tensor
        dim (int or tuple of int, optional): dimension to reduce
        keepdim (bool, optional): whether retain ``dim`` or not
    """
    import torch
    
    # Create a mask for non-nan values
    mask = ~torch.isnan(input)
    
    # Replace nan values with 0 for computation
    input_clean = torch.where(mask, input, torch.tensor(0.0, dtype=input.dtype, device=input.device))
    
    if dim is None:
        # Compute mean over all elements
        total_sum = torch.sum(input_clean)
        count = torch.sum(mask.float())
        return total_sum / count
    else:
        # Compute mean over specified dimension(s)
        total_sum = torch.sum(input_clean, dim=dim, keepdim=keepdim)
        count = torch.sum(mask.float(), dim=dim, keepdim=keepdim)
        return total_sum / count