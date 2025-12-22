import numbers
import torch
import torch.nn as nn
from fastdm.kernel.operators_set import rms_norm

class RMSNorm:
    def __init__(self, dim, eps: float, elementwise_affine: bool = True):
        super().__init__()

        self.eps = eps

        if isinstance(dim, numbers.Integral):
            dim = (dim,)

        self.dim = torch.Size(dim)

        if elementwise_affine:
            self.weight = nn.Parameter(torch.ones(dim))
        else:
            self.weight = None

        self.elementwise_affine = elementwise_affine

    def forward(self, hidden_states):
        if self.weight is None:
            input_dtype = hidden_states.dtype
            variance = hidden_states.to(torch.float32).pow(2).mean(-1, keepdim=True)
            hidden_states = hidden_states * torch.rsqrt(variance + self.eps)
            hidden_states = hidden_states.to(input_dtype)
        else:
            hidden_states = rms_norm(hidden_states, self.weight, self.eps)

        return hidden_states