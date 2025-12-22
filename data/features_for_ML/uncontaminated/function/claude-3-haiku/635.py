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
    original_params = sum(p.numel() for p in original_model.parameters())
    pruned_params = sum(p.numel() for p in pruned_model.parameters())
    
    original_nonzero_params = sum(torch.count_nonzero(p) for p in original_model.parameters())
    pruned_nonzero_params = sum(torch.count_nonzero(p) for p in pruned_model.parameters())
    
    pruning_ratio = 1 - pruned_params / original_params
    sparsity = 1 - pruned_nonzero_params / original_nonzero_params
    
    return {
        "original_params": original_params,
        "pruned_params": pruned_params,
        "original_nonzero_params": original_nonzero_params,
        "pruned_nonzero_params": pruned_nonzero_params,
        "pruning_ratio": pruning_ratio,
        "sparsity": sparsity,
    }