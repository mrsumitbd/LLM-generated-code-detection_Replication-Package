def save_pretrained(args: CkptConverterConfig):
    """Save a pretrained model from checkpoint converter configuration."""
    import os
    import json
    import torch
    from pathlib import Path
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the checkpoint
    if args.checkpoint_path:
        checkpoint = torch.load(args.checkpoint_path, map_location='cpu')
    else:
        checkpoint = {}
    
    # Extract model state dict
    if isinstance(checkpoint, dict):
        if 'model' in checkpoint:
            state_dict = checkpoint['model']
        elif 'state_dict' in checkpoint:
            state_dict = checkpoint['state_dict']
        else:
            state_dict = checkpoint
    else:
        state_dict = checkpoint
    
    # Save the model state dict
    model_path = output_dir / 'pytorch_model.bin'
    torch.save(state_dict, model_path)
    
    # Save config if available
    if hasattr(args, 'config') and args.config:
        config_path = output_dir / 'config.json'
        if isinstance(args.config, dict):
            with open(config_path, 'w') as f:
                json.dump(args.config, f, indent=2)
        elif isinstance(args.config, str) and os.path.exists(args.config):
            with open(args.config, 'r') as src:
                config_data = json.load(src)
            with open(config_path, 'w') as dst:
                json.dump(config_data, dst, indent=2)
    
    # Save tokenizer if available
    if hasattr(args, 'tokenizer_path') and args.tokenizer_path and os.path.exists(args.tokenizer_path):
        import shutil
        tokenizer_files = ['tokenizer.model', 'tokenizer.json', 'special_tokens_map.json', 
                          'tokenizer_config.json', 'vocab.txt']
        for fname in tokenizer_files:
            src_path = os.path.join(args.tokenizer_path, fname)
            if os.path.exists(src_path):
                dst_path = output_dir / fname
                shutil.copy2(src_path, dst_path)
    
    # Save metadata
    metadata = {
        'checkpoint_path': str(args.checkpoint_path) if args.checkpoint_path else None,
        'output_dir': str(args.output_dir),
    }
    
    if hasattr(args, 'model_name'):
        metadata['model_name'] = args.model_name
    if hasattr(args, 'model_type'):
        metadata['model_type'] = args.model_type
    
    metadata_path = output_dir / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Model saved to {output_dir}")