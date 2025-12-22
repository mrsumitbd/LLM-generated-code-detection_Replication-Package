def bgr_to_rgb(tensor_img):
    """Convert a PyTorch tensor image from BGR to RGB format.

    Args:
        tensor_img: Tensor in format (C, H, W) with values in [0, 1]
    """
    return tensor_img[[2, 1, 0], :, :]