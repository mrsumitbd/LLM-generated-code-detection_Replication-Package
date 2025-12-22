def load_ip_adapter_tensors(ip_adapter_ckpt_path: pathlib.Path, device: str) -> IPAdapterStateDict:
    import torch
    
    # Load the checkpoint
    checkpoint = torch.load(str(ip_adapter_ckpt_path), map_location=device)
    
    # Extract the state dict if it's wrapped in a model
    if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
        state_dict = checkpoint['state_dict']
    else:
        state_dict = checkpoint
    
    # Move tensors to the specified device
    ip_adapter_state_dict = {}
    for key, value in state_dict.items():
        if isinstance(value, torch.Tensor):
            ip_adapter_state_dict[key] = value.to(device)
        else:
            ip_adapter_state_dict[key] = value
    
    return ip_adapter_state_dict