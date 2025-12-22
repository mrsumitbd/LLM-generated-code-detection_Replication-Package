import torch

def tensor2mask(t: torch.Tensor) -> torch.Tensor:
    """
    Converts a tensor to a binary mask tensor.
    
    Args:
        t (torch.Tensor): The input tensor.
        
    Returns:
        torch.Tensor: The binary mask tensor.
    """
    return (t != 0).float()