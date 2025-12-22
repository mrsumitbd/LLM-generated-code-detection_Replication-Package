import numpy as np

def make_2d_mask(mask):
    """
    Convert a 1‑D mask (boolean or truthy values) into a 2‑D mask suitable for
    selecting a sub‑matrix. The resulting mask has shape (N, N) where N is the
    length of the input mask, and each element is the logical AND of the
    corresponding elements in the input mask.

    Parameters
    ----------
    mask : array‑like
        1‑D array of booleans or truthy values.

    Returns
    -------
    np.ndarray
        2‑D boolean mask of shape (N, N).
    """
    # Ensure we have a 1‑D boolean array
    mask = np.asarray(mask, dtype=bool).ravel()
    # Broadcast to 2‑D by outer product
    return np.outer(mask, mask)