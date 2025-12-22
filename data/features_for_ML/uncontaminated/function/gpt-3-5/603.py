def gelu_and_mul_cuda(x):
    import torch
    d = x.shape[-1] // 2
    return x[:, :d] * torch.nn.functional.gelu(x[:, d:])