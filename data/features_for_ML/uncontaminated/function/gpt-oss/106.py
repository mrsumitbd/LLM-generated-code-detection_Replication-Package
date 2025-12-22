import numpy as np

def reorder_image(img, input_order='HWC'):
    """Reorder images to 'HWC' order.

    If the input_order is (h, w), return (h, w, 1);
    If the input_order is (c, h, w), return (h, w, c);
    If the input_order is (h, w, c), return as it is.

    Args:
        img (ndarray): Input image.
        input_order (str): Whether the input order is 'HWC' or 'CHW'.
            If the input image shape is (h, w), input_order will not have
            effects. Default: 'HWC'.

    Returns:
        ndarray: reordered image.
    """
    # Ensure we are working with a NumPy array
    img = np.asarray(img)

    # Handle grayscale images (2D)
    if img.ndim == 2:
        # Add a singleton channel dimension
        return img[..., None]

    # Handle 3D images
    if img.ndim == 3:
        if input_order.upper() == 'CHW':
            # Convert from (C, H, W) to (H, W, C)
            return img.transpose(1, 2, 0)
        # If input_order is 'HWC' or any other, return as is
        return img

    # For any other dimensionality, return the image unchanged
    return img