import torch

def compute_neuron_pair_importance_vow(gate_weight: torch.Tensor, up_weight: torch.Tensor) -> torch.Tensor:
    gate_weight_mean = gate_weight.mean(dim=0)
    up_weight_mean = up_weight.mean(dim=0)
    
    importance_scores = torch.var(gate_weight_mean.unsqueeze(1) * up_weight_mean.unsqueeze(0), unbiased=False)
    
    return importance_scores