import torch

def apply_gate(x, gate, tr_gate=None, tr_token=None):
    if tr_gate is not None:
        x_zero = x[:, :tr_token] * tr_gate.unsqueeze(1)
        x_orig = x[:, tr_token:] * gate.unsqueeze(1)
        return torch.concat((x_zero, x_orig), dim=1)
    else:
        return x * gate.unsqueeze(1)