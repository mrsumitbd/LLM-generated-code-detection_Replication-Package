import torch

def onnx_compatible_tril(input_tensor: torch.Tensor, *args, **kwargs) -> torch.Tensor:
    """
    Returns the lower triangular part of a tensor, compatible with ONNX export.
    
    This function extracts the lower triangular portion of a 2D or higher dimensional tensor.
    For tensors with more than 2 dimensions, the operation is applied to the last two dimensions.
    """
    # Get the diagonal offset if provided
    diagonal = kwargs.get('diagonal', 0)
    
    # Use torch.tril which is ONNX compatible
    return torch.tril(input_tensor, diagonal=diagonal)