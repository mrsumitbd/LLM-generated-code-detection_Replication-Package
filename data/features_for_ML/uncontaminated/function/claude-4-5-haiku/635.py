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
    def count_parameters(model):
        total = 0
        trainable = 0
        for param in model.parameters():
            total += param.numel()
            if param.requires_grad:
                trainable += param.numel()
        return total, trainable
    
    def count_nonzero_parameters(model):
        total = 0
        for param in model.parameters():
            total += torch.count_nonzero(param).item()
        return total
    
    original_total, original_trainable = count_parameters(original_model)
    pruned_total, pruned_trainable = count_parameters(pruned_model)
    
    original_nonzero = count_nonzero_parameters(original_model)
    pruned_nonzero = count_nonzero_parameters(pruned_model)
    
    parameters_removed = original_total - pruned_total
    parameters_pruned = original_nonzero - pruned_nonzero
    
    pruning_ratio = (parameters_pruned / original_nonzero * 100) if original_nonzero > 0 else 0
    compression_ratio = (original_total / pruned_total) if pruned_total > 0 else float('inf')
    
    statistics = {
        "original_total_parameters": original_total,
        "original_trainable_parameters": original_trainable,
        "original_nonzero_parameters": original_nonzero,
        "pruned_total_parameters": pruned_total,
        "pruned_trainable_parameters": pruned_trainable,
        "pruned_nonzero_parameters": pruned_nonzero,
        "parameters_removed": parameters_removed,
        "parameters_pruned": parameters_pruned,
        "pruning_ratio_percent": pruning_ratio,
        "compression_ratio": compression_ratio,
        "sparsity_percent": (1 - pruned_nonzero / original_nonzero * 100) if original_nonzero > 0 else 0,
    }
    
    return statistics