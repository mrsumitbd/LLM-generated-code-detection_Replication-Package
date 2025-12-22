import torch
from typing import Tensor, Union, IO, Any
from easy_io import save_video, save_image

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
    if tensor.ndim == 5:
        batch_size, channels, time_steps, height, width = tensor.shape
    elif tensor.ndim == 4:
        channels, time_steps, height, width = tensor.shape
        batch_size = 1
    else:
        raise ValueError("Input tensor must have 4 or 5 dimensions.")

    if tensor.min() < -1 or tensor.max() > 1:
        tensor = (tensor - tensor.min()) / (tensor.max() - tensor.min())

    if n_views > 1:
        tensor = tensor.view(batch_size, channels, time_steps, n_views, height, width // n_views)
        tensor = tensor.permute(0, 1, 3, 2, 4, 5).contiguous().view(batch_size * n_views, channels, time_steps, height, width // n_views)

    if tensor.shape[2] > 1:
        save_video(tensor, save_path, fps=fps, ffmpeg_params=ffmpeg_params)
    else:
        save_image(tensor[0], save_path, quality=quality)