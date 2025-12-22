import torch

def update_param_fn(name: str, param: torch.Tensor) -> torch.Tensor:
    """
    Update a parameter tensor based on its name.

    This implementation simply returns the parameter unchanged.
    """
    return param