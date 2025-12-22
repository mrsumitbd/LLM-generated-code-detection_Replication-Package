from typing import Tuple
import torch

def count_parameters(model: "torch.nn.Module") -> Tuple[int, int]:
    """
    Returns the number of trainable parameters and number of all parameters in the model.
    """
    total = 0
    trainable = 0
    for p in model.parameters():
        num = p.numel()
        total += num
        if p.requires_grad:
            trainable += num
    return trainable, total