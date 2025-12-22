import torch
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Union
from megatron.core import parallel_state
from torch._utils import _flatten_dense_tensors, _unflatten_dense_tensors

def _allreduce_layernorm_grads(model: List[torch.nn.Module]):
    """
    All-reduce the following layernorm grads:
    - When tensor parallel is enabled, all-reduce grads of QK-layernorm
    - When sequence parallel, all-reduce grads of AdaLN, t_embedder, additional_timestamp_embedder,
    and affline_norm.
    """
    sequence_parallel = getattr(parallel_state, "sequence_parallel", False)

    if parallel_state.get_tensor_model_parallel_world_size() > 1:
        grads = []
        for model_chunk in model:
            for name, param in model_chunk.named_parameters():
                if not param.requires_grad:
                    continue

                if "to_q.1" in name or "to_k.1" in name:  # TP  # Q-layernorm  # K-layernorm
                    grad = param.grad
                    if grad is not None:
                        grads.append(grad.data)

                if sequence_parallel:  # TP + SP
                    if (
                        "t_embedder" in name
                        or "adaLN_modulation" in name
                        or "additional_timestamp_embedder" in name
                        or "affline_norm" in name
                        or "input_hint_block" in name
                        or "zero_blocks" in name
                    ):
                        grad = param.grad
                        if grad is not None:
                            grads.append(grad.data)

        if grads:
            coalesced = _flatten_dense_tensors(grads)
            torch.distributed.all_reduce(coalesced, group=parallel_state.get_tensor_model_parallel_group())
            for buf, synced in zip(grads, _unflatten_dense_tensors(coalesced, grads)):
                buf.copy_(synced)