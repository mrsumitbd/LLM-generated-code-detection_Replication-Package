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

    Returns:
        np.ndarray: Cropped image.
    """
    return img[top:bottom, left:right, ...]