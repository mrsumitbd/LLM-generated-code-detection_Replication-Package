def _list_checkpoint_files(model_id: Optional[str] = None) -> List[str]:
    """
    Core implementation of listing checkpoint files.

    Args:
        model_id: Optional model identifier to filter checkpoints

    Returns:
        List of checkpoint paths
    """
    import os
    from pathlib import Path
    
    checkpoint_dirs = [
        Path.home() / ".cache" / "huggingface" / "hub",
        Path.cwd() / "checkpoints",
        Path.cwd() / ".checkpoints",
    ]
    
    checkpoint_files = []
    
    for checkpoint_dir in checkpoint_dirs:
        if not checkpoint_dir.exists():
            continue
            
        for root, dirs, files in os.walk(checkpoint_dir):
            for file in files:
                if file.endswith(('.pt', '.pth', '.bin', '.safetensors', '.ckpt')):
                    file_path = os.path.join(root, file)
                    
                    if model_id is None:
                        checkpoint_files.append(file_path)
                    elif model_id.lower() in file_path.lower():
                        checkpoint_files.append(file_path)
    
    return sorted(checkpoint_files)