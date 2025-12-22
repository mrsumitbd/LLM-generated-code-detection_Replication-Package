def convert_to_audio(multiframe, count):
    """
    Optimized version of convert_to_audio that eliminates inefficient tensor operations
    and reduces CPU-GPU transfers for much faster inference on high-end GPUs.
    """
    import torch
    import numpy as np
    
    # Ensure multiframe is a tensor
    if not isinstance(multiframe, torch.Tensor):
        multiframe = torch.tensor(multiframe, dtype=torch.float32)
    
    # Get device (GPU if available, else CPU)
    device = multiframe.device if isinstance(multiframe, torch.Tensor) else torch.device('cpu')
    
    # Ensure multiframe is on the correct device
    if isinstance(multiframe, torch.Tensor):
        multiframe = multiframe.to(device)
    else:
        multiframe = torch.tensor(multiframe, dtype=torch.float32, device=device)
    
    # Handle batch dimension if needed
    if multiframe.dim() == 2:
        multiframe = multiframe.unsqueeze(0)
    
    # Normalize to [-1, 1] range if needed
    max_val = torch.max(torch.abs(multiframe))
    if max_val > 0:
        multiframe = multiframe / max_val
    
    # Ensure values are in valid audio range
    multiframe = torch.clamp(multiframe, -1.0, 1.0)
    
    # Convert to numpy for audio processing (keep on GPU if possible)
    if device.type == 'cuda':
        audio_data = multiframe.cpu().numpy()
    else:
        audio_data = multiframe.numpy()
    
    # Flatten to 1D audio
    audio_data = audio_data.flatten()
    
    # Convert to int16 for standard audio format
    audio_data = (audio_data * 32767).astype(np.int16)
    
    return audio_data