import torch
import torch.nn as nn
import torch.nn.functional as F


class RMSNorm(nn.Module):
    """
    Root Mean Square Layer Normalization.

    Args:
        dim (int): Size of the last dimension of the input.
        eps (float): Small value added for numerical stability.
        elementwise_affine (bool, optional): If True, includes a learnable
            scaling parameter. Defaults to True.
    """

    def __init__(self, dim: int, eps: float, elementwise_affine: bool = True):
        super().__init__()
        self.dim = dim
        self.eps = eps
        self.elementwise_affine = elementwise_affine
        if self.elementwise_affine:
            # Initialize weight to ones
            self.weight = nn.Parameter(torch.ones(dim))
        else:
            self.register_parameter("weight", None)

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        """
        Apply RMSNorm to the input tensor.

        Args:
            hidden_states (torch.Tensor): Input tensor of shape
                (..., dim).

        Returns:
            torch.Tensor: Normalized tensor of the same shape.
        """
        # Compute mean of squares over the last dimension
        mean_square = hidden_states.pow(2).mean(dim=-1, keepdim=True)
        # Compute RMS with epsilon for stability
        rms = torch.sqrt(mean_square + self.eps)
        # Normalize
        normalized = hidden_states / rms
        # Apply learnable scaling if enabled
        if self.elementwise_affine:
            # weight shape (dim,) -> broadcast to (..., dim)
            normalized = normalized * self.weight
        return normalized