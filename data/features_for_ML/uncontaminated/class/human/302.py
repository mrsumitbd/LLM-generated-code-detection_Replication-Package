from typing import Dict, Optional, Tuple, Union
import torch

class CheckpointState:
    """State of model, optimizer, and scheduler after a given number of epochs."""

    model: torch.nn.Module
    optimizer: torch.optim.Optimizer
    lr_scheduler: torch.optim.lr_scheduler._LRScheduler = None  # Optional
    best_loss: Union[torch.Tensor, None] = torch.tensor([])