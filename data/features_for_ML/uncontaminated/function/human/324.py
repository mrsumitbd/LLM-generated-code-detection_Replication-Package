import torch

def onnx_compatible_tril(input_tensor: torch.Tensor, *args, **kwargs) -> torch.Tensor:
    if input_tensor.dtype == torch.int32:
        return original_tril(input_tensor.to(torch.int64), *args, **kwargs).to(torch.int32)
    else:
        return original_tril(input_tensor, *args, **kwargs)