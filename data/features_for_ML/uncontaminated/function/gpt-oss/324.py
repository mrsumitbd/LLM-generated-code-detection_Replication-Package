import torch

def onnx_compatible_tril(input_tensor: torch.Tensor, *args, **kwargs) -> torch.Tensor:
    """
    Return the lower triangular part of `input_tensor`, compatible with ONNX export.

    Parameters
    ----------
    input_tensor : torch.Tensor
        The input tensor.
    *args, **kwargs
        Arguments forwarded to `torch.tril`. Typically includes `diagonal`.

    Returns
    -------
    torch.Tensor
        The lower triangular matrix.
    """
    # Directly use torch.tril which is ONNX‑exportable.
    return torch.tril(input_tensor, *args, **kwargs)