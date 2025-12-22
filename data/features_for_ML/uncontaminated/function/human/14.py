import numpy as np
from transformers.image_utils import (
    ChannelDimension,
    ImageInput,
    PILImageResampling,
    get_image_size,
    infer_channel_dimension_format,
    is_scaled_image,
    make_flat_list_of_images,
    to_numpy_array,
    valid_images,
    validate_preprocess_arguments,
)

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
    if not isinstance(img, np.ndarray):
        raise TypeError('img should be numpy array. Got {}'.format(type(img)))

    if img.ndim not in [2, 3]:
        raise ValueError('Image should have 2 or 3 dimensions. Got {}'.format(img.ndim))

    if input_data_format == ChannelDimension.LAST:
        img_height = img.shape[0]
        img_width = img.shape[1]
    else:
        img_height = img.shape[1]
        img_width = img.shape[2]

    if top < 0 or left < 0 or bottom > img_height or right > img_width:
        raise ValueError('Crop coordinates out of bounds')

    if top >= bottom or left >= right:
        raise ValueError('Invalid crop coordinates')
    if input_data_format == ChannelDimension.LAST:
        return img[top:bottom, left:right, :]
    else:
        return img[:, top:bottom, left:right]