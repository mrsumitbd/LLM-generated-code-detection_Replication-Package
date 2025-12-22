import torch

def mask_to_bias(mask: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
    """
    Converts a boolean mask tensor to a bias tensor.

    Args:
        mask (torch.Tensor): A boolean tensor.
        dtype (torch.dtype): The desired data type of the output tensor.

    Returns:
        torch.Tensor: A tensor of the same shape as the input mask, with values of 0.0 where the mask is True, and a large negative value where the mask is False.
    """
    bias = torch.full_like(mask, float('-inf'), dtype=dtype)
    bias[mask] = 0.0
    return bias