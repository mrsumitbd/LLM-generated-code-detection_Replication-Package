import torch.distributed as dist

def _allreduce_layernorm_grads(model: List[torch.nn.Module]):
    """
    All-reduce the following layernorm grads:
    - When tensor parallel is enabled, all-reduce grads of QK-layernorm
    - When sequence parallel, all-reduce grads of AdaLN, t_embedder, additional_timestamp_embedder,
    and affline_norm.
    """
    for module in model:
        if isinstance(module, torch.nn.LayerNorm):
            if hasattr(module, "qk_layernorm"):
                dist.all_reduce(module.qk_layernorm.grad, op=dist.ReduceOp.SUM)
            if hasattr(module, "adaln"):
                dist.all_reduce(module.adaln.grad, op=dist.ReduceOp.SUM)
            if hasattr(module, "t_embedder"):
                dist.all_reduce(module.t_embedder.grad, op=dist.ReduceOp.SUM)
            if hasattr(module, "additional_timestamp_embedder"):
                dist.all_reduce(module.additional_timestamp_embedder.grad, op=dist.ReduceOp.SUM)
            if hasattr(module, "affline_norm"):
                dist.all_reduce(module.affline_norm.grad, op=dist.ReduceOp.SUM)