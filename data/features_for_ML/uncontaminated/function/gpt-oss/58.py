import torch

def compute_neuron_pair_importance_vow(gate_weight: torch.Tensor, up_weight: torch.Tensor) -> torch.Tensor:
    """
    Compute neuron pair importance scores using Variance of Weights method.

    Args:
        gate_weight: Weight matrix from the gate_proj layer (shape: [num_neurons, ...]).
        up_weight: Weight matrix from the up_proj layer (shape: [num_neurons, ...]).

    Returns:
        importance_scores: Importance scores for each neuron pair (shape: [num_neurons]).
    """
    # Ensure the weight matrices have the same shape
    if gate_weight.shape != up_weight.shape:
        raise ValueError("gate_weight and up_weight must have the same shape")

    # Compute variance across the feature dimension for each neuron (row)
    # Use unbiased=False for consistency with many pruning implementations
    gate_var = torch.var(gate_weight, dim=1, unbiased=False)
    up_var   = torch.var(up_weight,   dim=1, unbiased=False)

    # Sum the variances to obtain the importance score for each neuron pair
    importance_scores = gate_var + up_var

    return importance_scores