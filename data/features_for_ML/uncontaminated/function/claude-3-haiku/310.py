def pad_to_length(tensor, length, pad_value, dim=-1):
    """
    Pads a tensor to a specified length along a given dimension.

    Args:
        tensor (torch.Tensor): The input tensor to be padded.
        length (int): The desired length of the tensor along the specified dimension.
        pad_value (float): The value to use for padding.
        dim (int, optional): The dimension along which to pad the tensor. Defaults to -1 (last dimension).

    Returns:
        torch.Tensor: The padded tensor.
    """
    if dim < 0:
        dim += tensor.ndim
    
    pad_size = [0] * (tensor.ndim * 2)
    pad_size[2 * dim + 1] = length - tensor.size(dim)
    
    return torch.nn.functional.pad(tensor, pad_size, value=pad_value)