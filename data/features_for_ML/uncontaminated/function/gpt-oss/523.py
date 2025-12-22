import torch

def mask_to_bias(mask: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
    """
    Convert a binary mask to an attention bias tensor.

    Parameters
    ----------
    mask : torch.Tensor
        Binary mask where 1 (or True) indicates a valid position and 0 (or False)
        indicates a masked position. The mask can be of any shape that is
        broadcastable to the attention logits shape.
    dtype : torch.dtype
        Desired data type of the returned bias tensor.

    Returns
    -------
    torch.Tensor
        A tensor of the same shape as `mask` (broadcasted to the logits shape)
        where valid positions have a bias of 0 and masked positions have a
        large negative bias (approximately -1e9) suitable for use in softmax
        based attention mechanisms.
    """
    # Ensure mask is float for arithmetic, then cast to desired dtype
    mask_float = mask.to(dtype)
    # Compute bias: 0 for valid (mask==1), -1e9 for masked (mask==0)
    bias = (1.0 - mask_float) * -1e9
    return bias