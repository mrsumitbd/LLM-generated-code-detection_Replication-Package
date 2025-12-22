import torch
import torch.nn as nn
from torch.distributed import broadcast, get_rank, get_world_size


def broadcast_params(module):
    """
    Broadcast module parameters from rank 0 to all other ranks.
    
    This function synchronizes model parameters across all distributed processes
    by broadcasting them from rank 0 to all other ranks.
    
    Args:
        module: A PyTorch module whose parameters should be broadcasted
    """
    for param in module.parameters():
        broadcast(param.data, src=0)