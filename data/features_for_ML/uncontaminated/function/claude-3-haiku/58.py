import torch

def compute_neuron_pair_importance_vow(gate_weight: torch.Tensor, up_weight: torch.Tensor) -> torch.Tensor:
    """
    Compute neuron pair importance scores using Variance of Weights method.
    
    Args:
        gate_weight: Weight matrix from the gate_proj layer
        up_weight: Weight matrix from the up_proj layer
        
    Returns:
        importance_scores: Importance scores for each neuron pair
    """
    gate_weight_flat = gate_weight.flatten()
    up_weight_flat = up_weight.flatten()
    
    importance_scores = torch.abs(gate_weight_flat * up_weight_flat)
    
    return importance_scores