import numpy as np
from typing import Union

# Assuming ChannelDimension is defined elsewhere in the project.
# It should provide at least two members: HWC and CHW.
# If not available, you can replace the checks with string literals.
try:
    from .channel_dimension import ChannelDimension  # type: ignore
except Exception:
    # Fallback definition for type checking purposes
    class ChannelDimension:
        HWC = "HWC"
        CHW = "CHW"


def crop(
    img: np.ndarray,
    left: int,
    top: int,
    right: int,
    bottom: int,
    input_data_format: ChannelDimension,
) -> np.ndarray:
    """Crop the given numpy array.

    Args:
        img (np.ndarray): Image to be cropped. Format should be (H, W, C) or (H, W).
        left (int): The left coordinate of the crop box.
        top (int): The top coordinate of the crop box.
        right (int): The right coordinate of the crop box.
        bottom (int): The bottom coordinate of the crop box.
        input_data_format (ChannelDimension): Indicates the channel dimension layout.

    Returns:
        np.ndarray: Cropped image.
    """
    if img.ndim not in (2, 3):
        raise ValueError(f"Unsupported image shape {img.shape!r}. Expected 2 or 3 dimensions.")

    # Determine spatial dimensions
    if img.ndim == 2:
        h, w = img.shape
    else:  # 3D
        if input_data_format == ChannelDimension.HWC:
            h, w, _ = img.shape
        elif input_data_format == ChannelDimension.CHW:
            _, h, w = img.shape
        else:
            raise ValueError(f"Unsupported channel dimension layout: {input_data_format!r}")

    # Validate coordinates
    if left < 0 or top < 0 or right > w or bottom > h:
        raise ValueError(
            f"Crop coordinates out of bounds: left={left}, top={top}, right={right}, bottom={bottom}, "
            f"image size=({h}, {w})"
        )
    if right <= left or bottom <= top:
        raise ValueError(
            f"Invalid crop box: left={left}, top={top}, right={right}, bottom={bottom}"
        )

    # Perform cropping
    if img.ndim == 2:
        return img[top:bottom, left:right]
    else:  # 3D
        if input_data_format == ChannelDimension.HWC:
            return img[top:bottom, left:right, :]
        else:  # CHW
            return img[:, top:bottom, left:right]