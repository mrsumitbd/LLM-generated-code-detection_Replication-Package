def _compute_statistics(x, m, dim=2, eps=1e-5):
    mean = x.mean(dim, keepdim=True)
    x_centered = x - mean
    var = (x_centered ** 2).mean(dim, keepdim=True)
    std = (var + eps).sqrt()
    return mean, std