import torch

def pad_to_length(tensor: torch.Tensor, length: int, pad_value, dim: int = -1) -> torch.Tensor:
    """
    Pad or truncate a tensor along a specified dimension to a given length.

    Parameters
    ----------
    tensor : torch.Tensor
        Input tensor.
    length : int
        Desired length along the specified dimension.
    pad_value : scalar
        Value to use for padding.
    dim : int, optional
        Dimension along which to pad/truncate. Defaults to -1 (last dimension).

    Returns
    -------
    torch.Tensor
        Tensor padded or truncated to the specified length.
    """
    # Resolve negative dimension
    if dim < 0:
        dim += tensor.dim()
    # Current size along the dimension
    current = tensor.size(dim)

    # If the tensor is already the desired length, return it unchanged
    if current == length:
        return tensor

    # If the tensor is longer than desired, truncate it
    if current > length:
        return tensor.narrow(dim, 0, length)

    # Otherwise, pad the tensor at the end of the dimension
    pad_amount = length - current
    # Build a tensor of the same shape except for the padded dimension
    pad_shape = list(tensor.shape)
    pad_shape[dim] = pad_amount
    pad_tensor = torch.full(
        pad_shape,
        pad_value,
        dtype=tensor.dtype,
        device=tensor.device,
        layout=tensor.layout,
        requires_grad=tensor.requires_grad,
    )
    return torch.cat([tensor, pad_tensor], dim=dim)