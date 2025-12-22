def pad_to_length(tensor, length, pad_value, dim=-1):
    pad_size = length - tensor.size(dim)
    pad_shape = list(tensor.shape)
    pad_shape[dim] = pad_size
    padding = torch.full(pad_shape, pad_value, dtype=tensor.dtype, device=tensor.device)
    return torch.cat([tensor, padding], dim=dim)