import numpy as np

def rgb2ycbcr(img, y_only=False):
    """Convert a RGB image to YCbCr image.

    This function produces the same results as Matlab's `rgb2ycbcr` function.
    It implements the ITU-R BT.601 conversion for standard-definition
    television. See more details in
    https://en.wikipedia.org/wiki/YCbCr#ITU-R_BT.601_conversion.

    It differs from a similar function in cv2.cvtColor: `RGB <-> YCrCb`.
    In OpenCV, it implements a JPEG conversion. See more details in
    https://en.wikipedia.org/wiki/YCbCr#JPEG_conversion.

    Args:
        img (ndarray): The input image. It accepts:
            1. np.uint8 type with range [0, 255];
            2. np.float32 type with range [0, 1].
        y_only (bool): Whether to only return Y channel. Default: False.

    Returns:
        ndarray: The converted YCbCr image. The output image has the same type
            and range as input image.
    """
    if not isinstance(img, np.ndarray):
        raise TypeError("Input must be a numpy array")

    # Determine input type and scale
    if img.dtype == np.uint8:
        scale = 255.0
        img_f = img.astype(np.float32)
    elif img.dtype == np.float32:
        scale = 1.0
        img_f = img.astype(np.float32)
    else:
        raise TypeError("Input array must be of type uint8 or float32")

    # Ensure image has 3 channels
    if img_f.ndim != 3 or img_f.shape[2] != 3:
        raise ValueError("Input image must have shape (H, W, 3)")

    # Split channels
    R = img_f[..., 0]
    G = img_f[..., 1]
    B = img_f[..., 2]

    # ITU-R BT.601 conversion
    Y  =  0.299   * R + 0.587   * G + 0.114   * B
    Cb = -0.168736 * R - 0.331264 * G + 0.5     * B
    Cr =  0.5     * R - 0.418688 * G - 0.081312 * B

    # Scale back to original range
    Y  = Y  * scale
    Cb = Cb * scale
    Cr = Cr * scale

    # Clip to valid range
    Y  = np.clip(Y,  0, scale)
    Cb = np.clip(Cb, 0, scale)
    Cr = np.clip(Cr, 0, scale)

    if y_only:
        out = Y
    else:
        out = np.stack((Y, Cb, Cr), axis=-1)

    # Cast back to original dtype
    if img.dtype == np.uint8:
        out = np.rint(out).astype(np.uint8)
    else:
        out = out.astype(np.float32)

    return out