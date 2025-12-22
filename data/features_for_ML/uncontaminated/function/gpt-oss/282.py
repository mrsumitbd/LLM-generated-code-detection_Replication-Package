import torch

def bgr_to_rgb(tensor_img):
    """Convert a PyTorch tensor image from BGR to RGB format.

    Args:
        tensor_img: Tensor in format (C, H, W) with values in [0, 1]
    """
    if tensor_img.ndim != 3 or tensor_img.shape[0] != 3:
        raise ValueError("Input tensor must have shape (3, H, W)")
    return tensor_img[[2, 1, 0], :, :]