import torch

def _is_tensor_video_clip(clip):
    """
    Return True if `clip` is a torch.Tensor that represents a video clip.
    A video clip is expected to be a 4‑D tensor with either:
        - shape (T, H, W, C)  where C is 1 or 3
        - shape (C, T, H, W)  where C is 1 or 3
    """
    if not isinstance(clip, torch.Tensor):
        return False

    if clip.ndim != 4:
        return False

    # Check for (T, H, W, C) layout
    if clip.shape[3] in (1, 3):
        return True

    # Check for (C, T, H, W) layout
    if clip.shape[0] in (1, 3):
        return True

    return False