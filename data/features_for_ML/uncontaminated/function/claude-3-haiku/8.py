import torch

def create_and_permute_tensor(l, mode0, mode1, is_mode0_major, dtype, is_dynamic_layout=True):
    if is_mode0_major:
        tensor = torch.empty((mode0, mode1, l), dtype=dtype, layout=torch.strided if is_dynamic_layout else torch.contiguous_format)
    else:
        tensor = torch.empty((l, mode0, mode1), dtype=dtype, layout=torch.strided if is_dynamic_layout else torch.contiguous_format)
    return tensor.permute(1, 2, 0)