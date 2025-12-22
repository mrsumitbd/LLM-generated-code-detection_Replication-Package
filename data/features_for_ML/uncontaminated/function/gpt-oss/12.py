import torch

def broadcast_params(module):
    """
    Return a dictionary mapping parameter names to their data tensors.
    The tensors are cloned to avoid accidental in-place modifications.
    """
    return {name: param.data.clone() for name, param in module.named_parameters()}