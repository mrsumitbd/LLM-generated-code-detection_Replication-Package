def rgb2ycbcr_pt(img, y_only=False):
    """Convert RGB images to YCbCr images (PyTorch version).

    It implements the ITU-R BT.601 conversion for standard-definition television. See more details in
    https://en.wikipedia.org/wiki/YCbCr#ITU-R_BT.601_conversion.

    Args:
        img (Tensor): Images with shape (n, 3, h, w), the range [0, 1], float, RGB format.
         y_only (bool): Whether to only return Y channel. Default: False.

    Returns:
        (Tensor): converted images with the shape (n, 3/1, h, w), the range [0, 1], float.
    """
    import torch
    
    # ITU-R BT.601 conversion coefficients
    # Y = 0.299*R + 0.587*G + 0.114*B
    # Cb = -0.169*R - 0.331*G + 0.5*B + 0.5
    # Cr = 0.5*R - 0.419*G - 0.081*B + 0.5
    
    # Reshape for broadcasting: (n, 3, h, w) -> (n, 3, 1, 1) for coefficients
    r = img[:, 0:1, :, :]
    g = img[:, 1:2, :, :]
    b = img[:, 2:3, :, :]
    
    y = 0.299 * r + 0.587 * g + 0.114 * b
    
    if y_only:
        return y
    
    cb = -0.169 * r - 0.331 * g + 0.5 * b + 0.5
    cr = 0.5 * r - 0.419 * g - 0.081 * b + 0.5
    
    ycbcr = torch.cat([y, cb, cr], dim=1)
    
    return ycbcr