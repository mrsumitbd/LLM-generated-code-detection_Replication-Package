def _compute_statistics(x, m, dim=2, eps=1e-8):
    """
    Computes the mean, standard deviation, and variance of the input tensor `x` along the specified dimension `dim`.

    Args:
        x (torch.Tensor): The input tensor.
        m (torch.Tensor): The mean of the input tensor.
        dim (int, optional): The dimension along which to compute the statistics. Defaults to 2.
        eps (float, optional): A small value added to the denominator for numerical stability. Defaults to 1e-8.

    Returns:
        tuple: A tuple containing the mean, standard deviation, and variance of the input tensor.
    """
    mean = m
    var = torch.mean((x - mean.unsqueeze(dim))**2, dim=dim, keepdim=True)
    std = torch.sqrt(var + eps)
    return mean, std, var