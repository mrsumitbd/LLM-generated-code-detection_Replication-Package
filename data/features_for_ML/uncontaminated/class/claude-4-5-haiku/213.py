class RMSNorm:

    def __init__(self, dim, eps: float, elementwise_affine: bool = True):
        self.eps = eps
        self.dim = dim
        self.elementwise_affine = elementwise_affine
        if self.elementwise_affine:
            self.weight = np.ones(dim)
        else:
            self.weight = None

    def forward(self, hidden_states):
        import numpy as np
        
        # Calculate RMS (Root Mean Square)
        rms = np.sqrt(np.mean(hidden_states ** 2, axis=-1, keepdims=True) + self.eps)
        
        # Normalize
        normalized = hidden_states / rms
        
        # Apply weight if elementwise_affine is True
        if self.elementwise_affine and self.weight is not None:
            normalized = normalized * self.weight
        
        return normalized