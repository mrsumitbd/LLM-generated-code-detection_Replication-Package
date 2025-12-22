import torch
from typing import Dict, Any

def get_pruning_statistics(
    original_model: torch.nn.Module,
    pruned_model: torch.nn.Module,
) -> Dict[str, Any]:
    """
    Calculate statistics about the pruning operation.

    Args:
        original_model: Original model before pruning
        pruned_model: Model after pruning

    Returns:
        Dictionary containing pruning statistics
    """
    # Helper to compute zeros and nonzeros for a parameter tensor
    def _param_stats(param: torch.Tensor) -> Dict[str, int]:
        numel = param.numel()
        zeros = int((param == 0).sum().item())
        nonzeros = numel - zeros
        return {"zeros": zeros, "nonzeros": nonzeros, "numel": numel}

    # Overall statistics
    total_params = 0
    total_zeros = 0
    total_nonzeros = 0

    per_layer_stats: Dict[str, Dict[str, Any]] = {}

    # Iterate over named parameters in the pruned model
    for name, pruned_param in pruned_model.named_parameters():
        # Find the corresponding original parameter
        original_param = dict(original_model.named_parameters()).get(name)
        if original_param is None:
            # Skip parameters that don't exist in the original model
            continue

        # Compute stats for this layer
        layer_stats = _param_stats(pruned_param)
        per_layer_stats[name] = layer_stats

        # Accumulate totals
        total_params += layer_stats["numel"]
        total_zeros += layer_stats["zeros"]
        total_nonzeros += layer_stats["nonzeros"]

    # Compute overall sparsity
    sparsity = total_zeros / total_params if total_params > 0 else 0.0

    return {
        "total_params": total_params,
        "total_zeros": total_zeros,
        "total_nonzeros": total_nonzeros,
        "sparsity": sparsity,
        "per_layer": per_layer_stats,
    }