def mean_with_nan(input, dim=None, keepdim=False):
    import torch
    import numpy as np

    if dim is None:
        return torch.mean(input[~torch.isnan(input)])
    else:
        return torch.mean(input[~torch.isnan(input)], dim=dim, keepdim=keepdim)