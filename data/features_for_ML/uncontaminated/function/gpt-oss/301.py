import torch

def mean_with_nan(input, dim=None, keepdim=False):
    """
    Mean of a tensor. Ignore all nan values.

    Parameters:
        input (Tensor): input tensor
        dim (int or tuple of int, optional): dimension to reduce
        keepdim (bool, optional): whether retain ``dim`` or not
    """
    # Ensure input is a tensor
    if not isinstance(input, torch.Tensor):
        input = torch.as_tensor(input)

    # Create mask of non-NaN values
    mask = ~torch.isnan(input)

    # Replace NaNs with zero for summation
    zeroed = torch.where(mask, input, torch.zeros_like(input))

    # Sum over the specified dimensions
    if dim is None:
        total = zeroed.sum()
        count = mask.sum()
    else:
        total = zeroed.sum(dim=dim, keepdim=keepdim)
        count = mask.sum(dim=dim, keepdim=keepdim)

    # Compute mean; division by zero will produce NaN as desired
    mean = total / count
    return mean