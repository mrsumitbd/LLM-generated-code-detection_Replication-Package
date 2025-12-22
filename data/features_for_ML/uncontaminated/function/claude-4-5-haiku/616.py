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
        raise NotImplementedError(f"train_bias={train_bias} not supported. Must be one of 'none', 'lora_only', 'all'")
    
    lora_state_dict = {}
    
    for key, value in state_dict.items():
        # Include LoRA A and B matrices
        if "lora_A" in key or "lora_B" in key:
            lora_state_dict[key] = value
        # Handle bias based on train_bias setting
        elif "bias" in key:
            if train_bias == "all":
                lora_state_dict[key] = value
            elif train_bias == "lora_only":
                # Only include bias if it's from a LoRA layer
                if "lora_" in key:
                    lora_state_dict[key] = value
        # Handle head weights if train_head is True
        elif train_head and ("lm_head" in key or "scalar_head" in key):
            lora_state_dict[key] = value
    
    return lora_state_dict