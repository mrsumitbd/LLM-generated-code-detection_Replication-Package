from typing import Dict
import torch

def lora_state_dict_from_full_state_dict(
    state_dict: dict, train_bias: str = "none", train_head: bool = False
) -> Dict[str, torch.Tensor]:
    if train_bias not in ['none', 'lora_only', 'all']:
        raise NotImplementedError("Invalid train_bias value. Use 'none', 'lora_only', or 'all'.")

    lora_state_dict = {}
    for key, value in state_dict.items():
        if "lora" in key:
            if train_bias == "none":
                if "bias" not in key:
                    lora_state_dict[key] = value
            elif train_bias == "lora_only":
                if "bias" in key:
                    lora_state_dict[key] = value
            elif train_bias == "all":
                lora_state_dict[key] = value

        if train_head and ("lm_head" in key or "scalar_head" in key):
            lora_state_dict[key] = value

    return lora_state_dict