from __future__ import annotations

from typing import Any, IO, Union

import torch
from torch import Tensor

# Import easy_io lazily to avoid import errors if the library is not installed.
try:
    import easy_io
except ImportError as exc:
    raise ImportError(
        "The `easy_io` package is required for `save_image_or_video_multiview`. "
        "Install it via `pip install easy-io`."
    ) from exc


def save_image_or_video_multiview(
    tensor: Tensor,
    save_path: Union[str, IO[Any]],
    fps: int = 24,
    quality: Any = None,
    ffmpeg_params: Any = None,
    n_views: int = 1,
) -> None:
    """
    Split the tensor into `n_views`, stack them along the width dimension, and save as a video.

    Args:
        tensor (Tensor): Input tensor with shape (B, C, T, H, W) or (C, T, H, W) in [-1, 1] or [0, 1] range.
            If in [-1, 1] range, it will be automatically converted to [0, 1] range.
        save_path (Union[str, IO[Any]]): File path (with or without extension) or file-like object.
        fps (int): Frames per second for video. Default is 24.
        quality: Optional quality parameter for images (passed to easy_io).
        ffmpeg_params: Optional ffmpeg parameters for videos (passed to easy_io).
        n_views (int): Number of views to split the tensor into. Must divide the channel dimension.

    Returns:
        None
    """
    # Ensure tensor is float and on CPU
    if not tensor.is_floating_point():
        tensor = tensor.float()
    if tensor.device != torch.device("cpu"):
        tensor = tensor.cpu()

    # Handle input shape: (C, T, H, W) -> add batch dimension
    if tensor.ndim == 4:
        tensor = tensor.unsqueeze(0)  # shape (1, C, T, H, W)

    if tensor.ndim != 5:
        raise ValueError(
            f"Expected tensor of shape (B, C, T, H, W) or (C, T, H, W), got shape {tensor.shape}"
        )

    B, C, T, H, W = tensor.shape

    # Convert from [-1, 1] to [0, 1] if needed
    if tensor.min() < 0 or tensor.max() > 1:
        tensor = (tensor + 1) / 2

    # Validate n_views
    if n_views <= 0:
        raise ValueError(f"n_views must be positive, got {n_views}")
    if C % n_views != 0:
        raise ValueError(
            f"Channel dimension {C} is not divisible by n_views {n_views}"
        )

    # Split channels into views
    views = torch.chunk(tensor, n_views, dim=1)  # each view shape (B, C_view, T, H, W)

    # Permute each view to (B, T, H, W, C_view)
    views = [v.permute(0, 2, 3, 4, 1) for v in views]

    # Concatenate views horizontally along width dimension
    composite = torch.cat(views, dim=3)  # shape (B, T, H, n_views*W, C_view)

    # If the output has a single channel, duplicate to 3 channels for video
    if composite.shape[-1] == 1:
        composite = composite.repeat(1, 1, 1, 1, 3)

    # Ensure values are in [0, 1]
    composite = torch.clamp(composite, 0.0, 1.0)

    # If save_path is a string without extension, add .mp4
    if isinstance(save_path, str) and not any(save_path.endswith(ext) for ext in (".mp4", ".gif", ".mov", ".avi")):
        save_path = f"{save_path}.mp4"

    # Save using easy_io
    easy_io.save_video(
        composite,
        save_path,
        fps=fps,
        ffmpeg_params=ffmpeg_params,
        quality=quality,
    )