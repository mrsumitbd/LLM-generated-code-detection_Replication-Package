import torch
import torch.nn as nn
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transformers import PreTrainedModel
    from dataclasses import dataclass

def prepare_model_for_training(model: "PreTrainedModel", model_args: "ModelArguments") -> None:
    """
    Prepare the model for training by:
        (1) Casting all LayerNorm layers to float32.
        (2) Ensuring the output embedding layer requires gradients.
        (3) Upcasting the lm_head (if present) to float32 and requiring gradients.
    """
    # 1. Cast all LayerNorm layers to fp32
    for module in model.modules():
        if isinstance(module, nn.LayerNorm):
            # Cast weight and bias to fp32
            if module.weight is not None:
                module.weight.data = module.weight.data.to(torch.float32)
                module.weight.requires_grad = True
            if module.bias is not None:
                module.bias.data = module.bias.data.to(torch.float32)
                module.bias.requires_grad = True

    # 2. Make output embedding layer require grads
    try:
        out_emb = model.get_output_embeddings()
    except AttributeError:
        out_emb = None
    if out_emb is not None:
        for param in out_emb.parameters():
            param.requires_grad = True

    # 3. Upcast lm_head to fp32 and require grads
    if hasattr(model, "lm_head") and model.lm_head is not None:
        for param in model.lm_head.parameters():
            param.data = param.data.to(torch.float32)
            param.requires_grad = True