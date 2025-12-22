def _is_tensor_video_clip(clip):
    if not isinstance(clip, torch.Tensor):
        return False
    if clip.ndim != 5:
        return False
    if clip.size(-1) != 3:
        return False
    return True