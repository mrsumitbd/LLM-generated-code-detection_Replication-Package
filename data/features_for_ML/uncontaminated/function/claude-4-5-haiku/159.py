def from_pretrained(model_config):
    """Load a pretrained model from configuration."""
    import os
    import json
    from pathlib import Path
    
    # Handle string path input
    if isinstance(model_config, str):
        model_path = model_config
    else:
        model_path = model_config.get('model_path') or model_config.get('path')
    
    # Expand user path and make absolute
    model_path = os.path.expanduser(model_path)
    if not os.path.isabs(model_path):
        model_path = os.path.abspath(model_path)
    
    # Check if path exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path does not exist: {model_path}")
    
    # Load configuration file
    config_path = os.path.join(model_path, 'config.json')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Load model weights
    weights_path = os.path.join(model_path, 'model.pt')
    if not os.path.exists(weights_path):
        weights_path = os.path.join(model_path, 'pytorch_model.bin')
    if not os.path.exists(weights_path):
        weights_path = os.path.join(model_path, 'model.pth')
    
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Model weights not found in: {model_path}")
    
    # Import torch
    try:
        import torch
    except ImportError:
        raise ImportError("PyTorch is required to load pretrained models")
    
    # Load weights
    weights = torch.load(weights_path, map_location='cpu')
    
    return {
        'config': config,
        'weights': weights,
        'model_path': model_path
    }