from typing import Dict
import torch

def lora_state_dict_from_full_state_dict(
    state_dict: dict, train_bias: str = "none", train_head: bool = False
) -> Dict[str, torch.Tensor]:
    """Return state_dict with weights of LoRA's A and B matrices and with biases depending on the `bias` value.

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

    if train_bias not in ["none", "lora_only", "all"]:
        raise NotImplementedError

    if train_bias == "none":
        return {
            k: state_dict[k]
            for k in state_dict
            if "lora_" in k
            or (train_head and any((h_name in k for h_name in head_layers)))
        }
    elif train_bias == "all":
        return {
            k: state_dict[k]
            for k in state_dict
            if "lora_" in k
            or "bias" in k
            or (train_head and any((h_name in k for h_name in head_layers)))
        }
    elif train_bias == "lora_only":
        to_return = {}
        for k in state_dict:
            if "lora_" in k:
                to_return[k] = state_dict[k]
                bias_name = k.split("lora_")[0] + "bias"
                if bias_name in state_dict:
                    to_return[bias_name] = state_dict[bias_name]
            elif train_head and any((h_name in k for h_name in head_layers)):
                to_return[k] = state_dict[k]

        return to_return