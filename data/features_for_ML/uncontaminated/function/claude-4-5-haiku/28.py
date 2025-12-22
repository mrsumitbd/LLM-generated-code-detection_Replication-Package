def _allreduce_layernorm_grads(model: List[torch.nn.Module]):
    """
    All-reduce the following layernorm grads:
    - When tensor parallel is enabled, all-reduce grads of QK-layernorm
    - When sequence parallel, all-reduce grads of AdaLN, t_embedder, additional_timestamp_embedder,
    and affline_norm.
    """
    from torch.distributed import get_rank, get_world_size
    import torch.distributed as dist
    
    if not dist.is_available() or not dist.is_initialized():
        return
    
    world_size = get_world_size()
    if world_size == 1:
        return
    
    # List of module names to all-reduce grads for
    target_modules = [
        'qk_norm',  # QK-layernorm for tensor parallel
        'ada_ln',   # AdaLN for sequence parallel
        't_embedder',  # t_embedder for sequence parallel
        'additional_timestamp_embedder',  # additional_timestamp_embedder for sequence parallel
        'affine_norm'  # affine_norm for sequence parallel
    ]
    
    for module_list in model:
        for name, module in module_list.named_modules():
            # Check if this module's name contains any of the target module names
            should_allreduce = any(target in name.lower() for target in target_modules)
            
            if should_allreduce:
                # All-reduce gradients for parameters in this module
                for param in module.parameters():
                    if param.grad is not None:
                        dist.all_reduce(param.grad)
                        param.grad.div_(world_size)