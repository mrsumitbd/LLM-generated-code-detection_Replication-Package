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
    if input_order == 'HWC':
        return img
    elif input_order == 'CHW':
        return np.transpose(img, (1, 2, 0))
    elif len(img.shape) == 2:
        return np.expand_dims(img, axis=-1)
    else:
        raise ValueError(f"Invalid input_order: {input_order}")