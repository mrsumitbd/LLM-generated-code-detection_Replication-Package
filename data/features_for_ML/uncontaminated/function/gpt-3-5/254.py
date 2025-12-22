def _is_tensor_video_clip(clip):
    if not isinstance(clip, torch.Tensor):
        return False
    if clip.dim() != 5:
        return False
    return True