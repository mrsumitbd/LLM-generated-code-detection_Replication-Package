import numpy as np

def resize_landmark(landmark, w, h, new_w, new_h):
    """
    Rescale landmark coordinates from an original image size (w, h)
    to a new image size (new_w, new_h).

    Parameters
    ----------
    landmark : array-like or list
        Landmark coordinates. Can be a list of (x, y) tuples/lists,
        a 1‑D array of length 2, or a 2‑D array of shape (N, 2).
    w, h : float
        Original image width and height.
    new_w, new_h : float
        Target image width and height.

    Returns
    -------
    same type as input
        Rescaled landmark coordinates.
    """
    # Convert to numpy array for processing
    arr = np.asarray(landmark, dtype=float)

    # Handle single point (1‑D array of length 2)
    single_point = False
    if arr.ndim == 1 and arr.size == 2:
        single_point = True
        arr = arr.reshape(1, 2)

    # Rescale
    scale_x = new_w / w
    scale_y = new_h / h
    arr[:, 0] *= scale_x
    arr[:, 1] *= scale_y

    # Convert back to original shape/type
    if single_point:
        result = arr.reshape(2)
    else:
        # If original was a list of tuples/lists, return that format
        if isinstance(landmark, list):
            result = [tuple(pt) for pt in arr]
        else:
            result = arr

    return result