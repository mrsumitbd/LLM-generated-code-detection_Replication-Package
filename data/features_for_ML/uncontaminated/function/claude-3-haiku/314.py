import torch

def update_param_fn(name: str, param: torch.Tensor) -> torch.Tensor:
    """
    Updates the given parameter tensor based on the provided name.
    
    Args:
        name (str): The name of the parameter to be updated.
        param (torch.Tensor): The parameter tensor to be updated.
    
    Returns:
        torch.Tensor: The updated parameter tensor.
    """
    if name == "weight":
        return param.abs()
    elif name == "bias":
        return param.clamp(-1, 1)
    else:
        return param