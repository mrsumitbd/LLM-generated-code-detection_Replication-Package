import numpy as np
from PIL import Image

def check_input_image(input_image):
    """
    Validate and convert an input image to a NumPy array.

    Parameters
    ----------
    input_image : numpy.ndarray or PIL.Image.Image
        The image to validate. It may be a 2‑D (grayscale) or 3‑D (RGB/RGBA) array,
        or a PIL Image instance.

    Returns
    -------
    numpy.ndarray
        The validated image as a NumPy array with dtype uint8.

    Raises
    ------
    TypeError
        If the input is not a NumPy array or PIL Image.
    ValueError
        If the image has an unsupported shape or dtype, or contains out‑of‑range values.
    """
    # Convert PIL Image to NumPy array
    if isinstance(input_image, Image.Image):
        img = np.array(input_image)
    elif isinstance(input_image, np.ndarray):
        img = input_image
    else:
        raise TypeError("input_image must be a NumPy array or PIL.Image.Image")

    # Ensure array is 2D or 3D
    if img.ndim not in (2, 3):
        raise ValueError(f"Unsupported image dimensionality: {img.ndim}D")

    # If 3D, ensure channel dimension is 3 (RGB) or 4 (RGBA)
    if img.ndim == 3:
        if img.shape[2] not in (3, 4):
            raise ValueError(f"Unsupported channel count: {img.shape[2]}")
    else:  # 2D grayscale
        pass

    # Validate dtype and value range
    if img.dtype == np.uint8:
        # uint8 values should be in [0, 255]
        if img.min() < 0 or img.max() > 255:
            raise ValueError("uint8 image contains values outside [0, 255]")
    elif img.dtype == np.float32 or img.dtype == np.float64:
        # float images should be in [0, 1]
        if img.min() < 0.0 or img.max() > 1.0:
            raise ValueError("float image contains values outside [0.0, 1.0]")
        # Convert to uint8
        img = (img * 255).round().astype(np.uint8)
    else:
        raise TypeError(f"Unsupported image dtype: {img.dtype}")

    return img