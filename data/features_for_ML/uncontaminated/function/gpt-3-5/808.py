from typing import Any, IO
import torch
from torchvision.utils import make_grid
from PIL import Image
from torchvision.io import write_video

def save_image_or_video_multiview(
    tensor: torch.Tensor, save_path: str | IO[Any], fps: int = 24, quality=None, ffmpeg_params=None, n_views: int = 1
) -> None:
    if tensor.min() < 0:
        tensor = (tensor + 1) / 2
    if tensor.shape[0] == 1:
        tensor = tensor.repeat(n_views, 1, 1, 1)
    tensor = tensor.unsqueeze(1)
    tensor = make_grid(tensor, nrow=n_views)
    tensor = tensor.permute(1, 2, 0).mul(255).clamp(0, 255).to(torch.uint8)
    if save_path.endswith('.mp4'):
        write_video(save_path, tensor, fps=fps, video_codec='libx264', options=ffmpeg_params)
    else:
        img = Image.fromarray(tensor.cpu().numpy())
        img.save(save_path, quality=quality)