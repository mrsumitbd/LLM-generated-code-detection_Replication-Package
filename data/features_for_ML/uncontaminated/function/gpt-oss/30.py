import numpy as np

def sequence_mask(length, max_length=None):
    """
    Create a boolean mask for sequences of varying lengths.

    Parameters
    ----------
    length : array-like of shape (batch,)
        Lengths of each sequence in the batch.
    max_length : int, optional
        The maximum sequence length to mask. If None, it is set to the
        maximum value in `length`.

    Returns
    -------
    mask : np.ndarray of shape (batch, max_length)
        Boolean mask where True indicates a valid element and False
        indicates padding.
    """
    # Convert input to a NumPy array
    length = np.asarray(length, dtype=np.int64)

    # Determine the maximum length
    if max_length is None:
        max_length = int(length.max())

    # Create a 2D array of indices: shape (1, max_length)
    idx = np.arange(max_length, dtype=np.int64)

    # Broadcast and compare to generate the mask
    mask = idx < length[:, None]

    return mask