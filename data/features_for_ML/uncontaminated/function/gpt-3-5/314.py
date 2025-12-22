import torch

def update_param_fn(name: str, param: torch.Tensor) -> torch.Tensor:
    # Implementation of the function
    updated_param = param * 2
    return updated_param