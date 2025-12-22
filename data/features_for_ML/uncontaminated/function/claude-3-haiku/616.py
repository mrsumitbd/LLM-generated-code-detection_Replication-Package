from typing import Dict
import torch

def lora_state_dict_from_full_state_dict(
    state_dict: dict, train_bias: str = "none", train_head: bool = False
) -> Dict[str, torch.Tensor]:
    lora_state_dict = {}

    for key, value in state_dict.items():
        if "lora_A" in key or "lora_B" in key:
            lora_state_dict[key] = value
        elif "bias" in key:
            if train_bias == "all":
                lora_state_dict[key] = value
            elif train_bias == "lora_only" and ("lora_A" in key or "lora_B" in key):
                lora_state_dict[key] = value
        elif train_head and ("lm_head" in key or "scalar_head" in key):
            lora_state_dict[key] = value

    if train_bias not in ["none", "lora_only", "all"]:
        raise NotImplementedError(f"train_bias={train_bias} is not implemented.")

    return lora_state_dict