import torch
import torch.nn.functional as F

class RMSNorm:
    def __init__(self, dim, eps: float, elementwise_affine: bool = True):
        super().__init__()
        self.dim = dim
        self.eps = eps
        self.elementwise_affine = elementwise_affine
        if self.elementwise_affine:
            self.weight = torch.nn.Parameter(torch.ones(self.dim))
            self.bias = torch.nn.Parameter(torch.zeros(self.dim))
        else:
            self.register_parameter('weight', None)
            self.register_parameter('bias', None)

    def forward(self, hidden_states):
        norm = torch.sqrt(torch.mean(hidden_states ** 2, dim=-1, keepdim=True) + self.eps)
        if self.elementwise_affine:
            return hidden_states / norm * self.weight + self.bias
        else:
            return hidden_states / norm