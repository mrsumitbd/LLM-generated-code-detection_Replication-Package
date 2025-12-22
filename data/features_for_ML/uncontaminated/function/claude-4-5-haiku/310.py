import torch

def pad_to_length(tensor, length, pad_value, dim=-1):
    """
    Pad a tensor to a specified length along a given dimension.
    
    Args:
        tensor: Input tensor to pad
        length: Target length for the specified dimension
        pad_value: Value to use for padding
        dim: Dimension along which to pad (default: -1, the last dimension)
    
    Returns:
        Padded tensor with the specified dimension padded to the target length
    """
    # Normalize negative dimension
    if dim < 0:
        dim = tensor.ndim + dim
    
    # Get current size along the specified dimension
    current_size = tensor.shape[dim]
    
    # If already at or exceeds target length, return as is
    if current_size >= length:
        return tensor
    
    # Calculate padding needed
    pad_amount = length - current_size
    
    # Create padding tuple for torch.nn.functional.pad
    # pad expects padding in reverse dimension order (last dim first)
    # For dim=-1 (last), we need (pad_left, pad_right)
    # For dim=-2, we need (0, 0, pad_left, pad_right)
    # etc.
    
    # Build padding list from the end
    padding = [0] * (2 * tensor.ndim)
    # Set padding for the target dimension
    padding_idx = 2 * (tensor.ndim - 1 - dim) + 1  # Right padding index
    padding[padding_idx] = pad_amount
    
    # Use torch.nn.functional.pad
    import torch.nn.functional as F
    padded_tensor = F.pad(tensor, padding, value=pad_value)
    
    return padded_tensor