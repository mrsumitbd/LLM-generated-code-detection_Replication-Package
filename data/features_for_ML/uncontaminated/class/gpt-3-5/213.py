class RMSNorm:

    def __init__(self, dim, eps: float, elementwise_affine: bool = True):
        self.dim = dim
        self.eps = eps
        self.elementwise_affine = elementwise_affine

    def forward(self, hidden_states):
        if self.elementwise_affine:
            mean = hidden_states.mean(dim=self.dim, keepdim=True)
            var = hidden_states.var(dim=self.dim, unbiased=False, keepdim=True)
            hidden_states = (hidden_states - mean) / (var + self.eps).sqrt()
        else:
            mean = hidden_states.mean()
            var = hidden_states.var(unbiased=False)
            hidden_states = (hidden_states - mean) / (var + self.eps).sqrt()
        
        return hidden_states