from typing import Dict
import torch

def lora_state_dict_from_full_state_dict(
    state_dict: dict,
    train_bias: str = "none",
    train_head: bool = False,
) -> Dict[str, torch.Tensor]:
    """
    Return state_dict with weights of LoRA's A and B matrices and with biases depending on the `bias` value.

    Args:
        state_dict: nn.Module full state dict with LoRA weights
        train_bias:
            ``"none"``: state dict will not store bias weights,
            ``"lora_only"``: state dict will store bias weights only from LoRA layers,
            ``"all"``: state dict will store all bias weights.
        train_head: if True, state dict will contain weights for head (lm_head, or scalar_head).

    Returns:
        Weights and biases of LoRA layers

    Raises:
        NotImplementedError: if `bias` not in ['none', 'lora_only', 'all']
    """
    allowed_bias = {"none", "lora_only", "all"}
    if train_bias not in allowed_bias:
        raise NotImplementedError(
            f"train_bias must be one of {allowed_bias}, got {train_bias}"
        )

    lora_state = {}
    for key, value in state_dict.items():
        # Include LoRA A and B matrices
        if "lora_A" in key or "lora_B" in key:
            lora_state[key] = value
            continue

        # Handle biases
        if "bias" in key:
            if train_bias == "none":
                continue
            if train_bias == "lora_only" and "lora_" not in key:
                continue
            lora_state[key] = value
            continue

        # Include head weights if requested
        if train_head and ("lm_head" in key or "scalar_head" in key):
            lora_state[key] = value
            continue

    return lora_state