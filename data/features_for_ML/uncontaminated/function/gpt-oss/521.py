import torch
from collections.abc import Mapping, Sequence

def to_best_device(batch, device=get_best_device()):
    """
    Recursively move a batch (tensor, dict, list, tuple, etc.) to the specified device.
    """
    # If it's a tensor, move it directly
    if isinstance(batch, torch.Tensor):
        return batch.to(device)

    # If it's a mapping (e.g., dict), recurse on values
    if isinstance(batch, Mapping):
        return type(batch)({k: to_best_device(v, device) for k, v in batch.items()})

    # If it's a sequence but not a string/bytes, recurse on elements
    if isinstance(batch, Sequence) and not isinstance(batch, (str, bytes)):
        return type(batch)(to_best_device(v, device) for v in batch)

    # Otherwise, return as is
    return batch