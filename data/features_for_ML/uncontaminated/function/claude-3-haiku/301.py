import torch

def mean_with_nan(input, dim=None, keepdim=False):
    """
    Mean of a tensor. Ignore all nan values.

    Parameters:
        input (Tensor): input tensor
        dim (int or tuple of int, optional): dimension to reduce
        keepdim (bool, optional): whether retain ``dim`` or not
    """
    if dim is None:
        num_elements = torch.sum(~torch.isnan(input))
        return torch.sum(input[~torch.isnan(input)]) / num_elements
    else:
        if isinstance(dim, int):
            dim = (dim,)
        num_elements = torch.sum(~torch.isnan(input), dim=dim, keepdim=keepdim)
        return torch.sum(input, dim=dim, keepdim=keepdim) / num_elements