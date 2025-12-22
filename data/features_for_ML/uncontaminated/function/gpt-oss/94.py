import numpy as np

def sequence_mask(length, max_length=None):
    """
    Create a boolean mask for sequences of variable lengths.

    Parameters
    ----------
    length : array-like of shape (batch,)
        Lengths of each sequence in the batch.
    max_length : int, optional
        The maximum sequence length to mask. If None, it is set to the
        maximum value in `length`.

    Returns
    -------
    mask : ndarray of shape (batch, max_length)
        mask[i, j] is True if j < length[i], otherwise False.
    """
    # Convert to a NumPy array of integers
    length = np.asarray(length, dtype=np.int64)

    if length.ndim != 1:
        raise ValueError("`length` must be a 1‑D array of sequence lengths")

    if max_length is None:
        max_length = int(length.max())

    # Create a 2‑D grid of indices: shape (batch, max_length)
    seq_range = np.arange(max_length, dtype=np.int64)
    seq_range = np.expand_dims(seq_range, 0)  # shape (1, max_length)

    # Broadcast lengths to shape (batch, 1) and compare
    mask = seq_range < np.expand_dims(length, 1)

    return mask