import torch

def rgb2ycbcr_pt(img, y_only=False):
    """
    Convert RGB images to YCbCr images (PyTorch version).

    It implements the ITU-R BT.601 conversion for standard-definition television.
    See more details in https://en.wikipedia.org/wiki/YCbCr#ITU-R_BT.601_conversion.

    Args:
        img (Tensor): Images with shape (n, 3, h, w), the range [0, 1], float, RGB format.
        y_only (bool): Whether to only return Y channel. Default: False.

    Returns:
        Tensor: converted images with the shape (n, 3/1, h, w), the range [0, 1], float.
    """
    # Ensure input is float
    img = img.float()

    # Split channels
    R = img[:, 0, :, :]
    G = img[:, 1, :, :]
    B = img[:, 2, :, :]

    # ITU-R BT.601 conversion
    Y  = 0.299 * R + 0.587 * G + 0.114 * B
    Cb = 0.564 * (B - Y) + 0.5
    Cr = 0.713 * (R - Y) + 0.5

    # Clamp to [0, 1] to avoid tiny out-of-range values
    Y  = Y.clamp(0.0, 1.0)
    Cb = Cb.clamp(0.0, 1.0)
    Cr = Cr.clamp(0.0, 1.0)

    if y_only:
        return Y.unsqueeze(1)
    else:
        return torch.cat([Y.unsqueeze(1), Cb.unsqueeze(1), Cr.unsqueeze(1)], dim=1)