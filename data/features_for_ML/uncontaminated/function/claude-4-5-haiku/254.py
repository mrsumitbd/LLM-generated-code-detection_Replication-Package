def _is_tensor_video_clip(clip):
    import torch
    
    if not isinstance(clip, torch.Tensor):
        return False
    
    if clip.ndim < 3:
        return False
    
    return True