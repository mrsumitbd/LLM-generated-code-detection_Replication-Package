def _allreduce_layernorm_grads(model: List[torch.nn.Module]):
    qk_layernorm_grads = []
    adaln_grads = []
    t_embedder_grads = []
    additional_timestamp_embedder_grads = []
    affine_norm_grads = []

    for module in model:
        if hasattr(module, 'qk_layernorm'):
            qk_layernorm_grads.append(module.qk_layernorm.weight.grad)
            qk_layernorm_grads.append(module.qk_layernorm.bias.grad)
        if hasattr(module, 'adaln'):
            adaln_grads.append(module.adaln.weight.grad)
            adaln_grads.append(module.adaln.bias.grad)
        if hasattr(module, 't_embedder'):
            t_embedder_grads.append(module.t_embedder.weight.grad)
            t_embedder_grads.append(module.t_embedder.bias.grad)
        if hasattr(module, 'additional_timestamp_embedder'):
            additional_timestamp_embedder_grads.append(module.additional_timestamp_embedder.weight.grad)
            additional_timestamp_embedder_grads.append(module.additional_timestamp_embedder.bias.grad)
        if hasattr(module, 'affine_norm'):
            affine_norm_grads.append(module.affine_norm.weight.grad)
            affine_norm_grads.append(module.affine_norm.bias.grad)

    if torch.distributed.is_initialized():
        qk_layernorm_grads = [torch.distributed.all_reduce(grad) for grad in qk_layernorm_grads]
        adaln_grads = [torch.distributed.all_reduce(grad) for grad in adaln_grads]
        t_embedder_grads = [torch.distributed.all_reduce(grad) for grad in t_embedder_grads]
        additional_timestamp_embedder_grads = [torch.distributed.all_reduce(grad) for grad in additional_timestamp_embedder_grads]
        affine_norm_grads = [torch.distributed.all_reduce(grad) for grad in affine_norm_grads]