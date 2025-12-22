def create_and_permute_tensor(l, mode0, mode1, is_mode0_major, dtype, is_dynamic_layout=True):
    import torch
    
    if is_mode0_major:
        # Create tensor with shape (l, mode1, mode0)
        tensor = torch.randn(l, mode1, mode0, dtype=dtype)
        # Permute to (mode0, mode1, l)
        # (l, mode1, mode0) -> (mode0, mode1, l)
        # We need to move dimension 2 to position 0, dimension 1 to position 1, dimension 0 to position 2
        tensor = tensor.permute(2, 1, 0)
    else:
        # Create tensor with shape (l, mode0, mode1)
        tensor = torch.randn(l, mode0, mode1, dtype=dtype)
        # Permute to (mode0, mode1, l)
        # (l, mode0, mode1) -> (mode0, mode1, l)
        # We need to move dimension 1 to position 0, dimension 2 to position 1, dimension 0 to position 2
        tensor = tensor.permute(1, 2, 0)
    
    return tensor