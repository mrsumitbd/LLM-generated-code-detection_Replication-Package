import torch

def tensor2mask(t: torch.Tensor) -> torch.Tensor:
    """
    Convert a tensor to a binary mask by thresholding at 0.5.
    
    Args:
        t: Input tensor with values typically in range [0, 1]
    
    Returns:
        Binary mask tensor with values 0 or 1
    """
    return (t > 0.5).float()