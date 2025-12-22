import os
from typing import Any, Dict, List, Tuple, Union

import torch
from PIL import Image

try:
    # torchvision.io.read_video is available in torchvision >=0.13
    from torchvision.io import read_video
except Exception:
    read_video = None  # type: ignore


def _load_video_from_path(path: str) -> Tuple[torch.Tensor, float]:
    """
    Load a video from a local file path using torchvision.io.read_video.
    Returns a tuple (video_tensor, fps). The video tensor shape is (T, H, W, C).
    """
    if read_video is None:
        raise RuntimeError(
            "torchvision.io.read_video is not available. "
            "Please install torchvision >=0.13 to load videos."
        )
    video, audio, info = read_video(path, pts_unit="sec")
    fps = info.get("video_fps", 0.0)
    return video, fps


def _load_frames_from_paths(paths: List[str]) -> List[Image.Image]:
    """
    Load a list of image file paths into PIL Image objects.
    """
    frames = []
    for p in paths:
        if not os.path.exists(p):
            continue
        try:
            img = Image.open(p).convert("RGB")
            frames.append(img)
        except Exception:
            continue
    return frames


def fetch_video(
    ele: Dict[str, Any], return_video_sample_fps: bool = False
) -> Union[torch.Tensor, List[Image.Image], Tuple[torch.Tensor, float]]:
    """
    Fetch a video from the provided dictionary.

    Parameters
    ----------
    ele : dict
        Dictionary containing video information. Expected keys:
        - 'video_path' : str, path to a video file.
        - 'video_frames' : list[str], list of image file paths representing frames.
        - 'video_url' : str, URL to a video file (currently not supported).
    return_video_sample_fps : bool, optional
        If True and a video file is loaded, return a tuple (video_tensor, fps).
        Otherwise, return only the video tensor or list of frames.

    Returns
    -------
    torch.Tensor | list[Image.Image] | tuple[torch.Tensor, float]
        The loaded video tensor (T, H, W, C) or a list of PIL Image frames.
        If `return_video_sample_fps` is True and a video file is loaded,
        a tuple (video_tensor, fps) is returned.
    """
    # 1. Try to load from a video file path
    video_path = ele.get("video_path")
    if video_path and isinstance(video_path, str) and os.path.exists(video_path):
        try:
            video, fps = _load_video_from_path(video_path)
            if return_video_sample_fps:
                return video, fps
            return video
        except Exception:
            # fall back to other methods
            pass

    # 2. Try to load from a list of frame paths
    frame_paths = ele.get("video_frames")
    if frame_paths and isinstance(frame_paths, list):
        frames = _load_frames_from_paths(frame_paths)
        if frames:
            return frames

    # 3. Unsupported or missing data
    # Return an empty tensor or list to avoid breaking downstream code
    if return_video_sample_fps:
        return torch.empty((0, 0, 0, 0)), 0.0
    return torch.empty((0, 0, 0, 0))