import os
import numpy as np
from einops import rearrange
import torch
from typing import IO, Any
from torch import Tensor
from imaginaire.utils import log
from imaginaire.utils.easy_io import easy_io

def save_image_or_video_multiview(
    tensor: Tensor, save_path: str | IO[Any], fps: int = 24, quality=None, ffmpeg_params=None, n_views: int = 1
) -> None:
    """
    Split the tensor into n_views, stack them along the width dimension, and save as a video
        Args:
        tensor (Tensor): Input tensor with shape (B, C, T, H, W) or (C, T, H, W) in [-1, 1] or [0, 1] range.
            If in [-1, 1] range, it will be automatically converted to [0, 1] range.
        save_path (Union[str, IO[Any]]): File path (with or without extension) or file-like object.
        fps (int): Frames per second for video. Default is 24.
        quality: Optional quality parameter for images (passed to easy_io).
        ffmpeg_params: Optional ffmpeg parameters for videos (passed to easy_io).
    """
    # Handle batch dimension if present
    if tensor.ndim == 5:
        tensor = tensor[0]  # Take the first item from the batch

    assert tensor.ndim == 4, "Tensor must have shape (C, T, H, W) or (B, C, T, H, W)"
    assert isinstance(save_path, str) or hasattr(save_path, "write"), "save_path must be a string or file-like object"

    # Normalize to [0, 1] range
    if torch.is_floating_point(tensor):
        # Check if tensor is in [-1, 1] range (approximately)
        if tensor.min() < -0.5:
            # Convert from [-1, 1] to [0, 1]
            tensor = (tensor + 1.0) / 2.0
        tensor = tensor.clamp(0, 1)
    else:
        assert tensor.dtype == torch.uint8, "Only support uint8 tensor"
        tensor = tensor.float().div(255)

    kwargs = {}
    if quality is not None:
        kwargs["quality"] = quality
    if ffmpeg_params is not None:
        kwargs["ffmpeg_params"] = ffmpeg_params

    save_obj = (rearrange((tensor.cpu().float().numpy() * 255), "c (v t) h w -> t (v h) w c", v=n_views) + 0.5).astype(
        np.uint8
    )
    if isinstance(save_path, str):
        # Check if path already has an extension
        base, ext = os.path.splitext(save_path)
        if not ext:
            save_path = f"{base}.mp4"
    log.info(f"Saving video to {save_path} with fps {fps} and result shape {save_obj.shape}")
    easy_io.dump(save_obj, save_path, file_format="mp4", format="mp4", fps=fps, **kwargs)