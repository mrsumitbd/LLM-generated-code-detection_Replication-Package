import torch

def onnx_compatible_tril(input_tensor: torch.Tensor, *args, **kwargs) -> torch.Tensor:
    return torch.tril(input_tensor, *args, **kwargs)