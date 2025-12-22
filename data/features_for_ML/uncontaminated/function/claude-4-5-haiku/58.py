def compute_neuron_pair_importance_vow(gate_weight: torch.Tensor, up_weight: torch.Tensor) -> torch.Tensor:
    """
    Compute neuron pair importance scores using Variance of Weights method.
    
    Args:
        gate_weight: Weight matrix from the gate_proj layer
        up_weight: Weight matrix from the up_proj layer
        
    Returns:
        importance_scores: Importance scores for each neuron pair
    """
    # Compute variance across the input dimension (dim=1) for each output neuron
    gate_variance = torch.var(gate_weight, dim=1, unbiased=False)
    up_variance = torch.var(up_weight, dim=1, unbiased=False)
    
    # Compute importance as the product of variances for each neuron pair
    importance_scores = gate_variance * up_variance
    
    return importance_scores