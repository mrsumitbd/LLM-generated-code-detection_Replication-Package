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
    import numpy as np
    
    img_type = img.dtype
    img_np = img.astype(np.float32)
    
    if img_type == np.uint8:
        # Normalize to [0, 1]
        img_np = img_np / 255.0
    
    # ITU-R BT.601 conversion matrix
    # Y = 0.299*R + 0.587*G + 0.114*B
    # Cb = -0.169*R - 0.331*G + 0.5*B + 128
    # Cr = 0.5*R - 0.419*G - 0.081*B + 128
    
    if len(img_np.shape) == 2:
        # Grayscale image
        ycbcr = img_np
    else:
        # Color image
        r = img_np[..., 0]
        g = img_np[..., 1]
        b = img_np[..., 2]
        
        y = 0.299 * r + 0.587 * g + 0.114 * b
        
        if y_only:
            ycbcr = y
        else:
            cb = -0.169 * r - 0.331 * g + 0.5 * b + 0.5
            cr = 0.5 * r - 0.419 * g - 0.081 * b + 0.5
            
            ycbcr = np.stack([y, cb, cr], axis=-1)
    
    # Convert back to original dtype
    if img_type == np.uint8:
        ycbcr = np.round(ycbcr * 255.0).astype(np.uint8)
    else:
        ycbcr = ycbcr.astype(img_type)
    
    return ycbcr