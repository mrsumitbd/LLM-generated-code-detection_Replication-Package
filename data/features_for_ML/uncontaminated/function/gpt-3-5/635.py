def get_pruning_statistics(original_model: torch.nn.Module, pruned_model: torch.nn.Module) -> Dict[str, Any]:
    original_params = sum(p.numel() for p in original_model.parameters())
    pruned_params = sum(p.numel() for p in pruned_model.parameters())
    
    params_pruned = original_params - pruned_params
    pruning_ratio = params_pruned / original_params * 100
    
    return {
        'original_params': original_params,
        'pruned_params': pruned_params,
        'params_pruned': params_pruned,
        'pruning_ratio': pruning_ratio
    }