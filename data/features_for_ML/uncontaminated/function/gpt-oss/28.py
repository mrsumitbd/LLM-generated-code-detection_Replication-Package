import torch
import torch.distributed as dist
from typing import List

def _allreduce_layernorm_grads(model: List[torch.nn.Module]):
    """
    All-reduce the following layernorm grads:
    - When tensor parallel is enabled, all-reduce grads of QK-layernorm
    - When sequence parallel, all-reduce grads of AdaLN, t_embedder,
      additional_timestamp_embedder, and affline_norm.
    """
    if not dist.is_initialized():
        return

    world_size = dist.get_world_size()
    if world_size <= 1:
        return

    # Mapping of module class names to the parallelism type
    tensor_parallel_modules = {"QKLayerNorm"}
    sequence_parallel_modules = {
        "AdaLN",
        "TEmbedder",
        "AdditionalTimestampEmbedder",
        "AffineNorm",
    }

    for module in model:
        module_name = module.__class__.__name__

        # Skip modules that are not in either set
        if module_name not in tensor_parallel_modules and module_name not in sequence_parallel_modules:
            continue

        # All-reduce gradients of all parameters in the module
        for param in module.parameters():
            if param.grad is None:
                continue
            # Sum across all processes
            dist.all_reduce(param.grad, op=dist.ReduceOp.SUM)
            # Average the gradients
            param.grad.div_(world_size)