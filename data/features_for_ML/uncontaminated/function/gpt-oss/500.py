import random
from collections.abc import Sequence

def _get_length(item):
    """Return a reasonable length for an item."""
    try:
        return len(item)
    except Exception:
        # Fallback: treat as scalar
        return 1

def batch(data, batch_type='static', batch_size=16,
          max_frames_in_batch=12000, mode='train'):
    """
    Wrapper for static/dynamic batching.

    Parameters
    ----------
    data : list
        List of data items. Each item can be a sequence (list, tuple,
        numpy array, torch tensor, etc.) or any object that has a
        meaningful ``len``.
    batch_type : {'static', 'dynamic'}, default='static'
        Type of batching to perform.
    batch_size : int, default=16
        Number of items per batch for static batching.
    max_frames_in_batch : int, default=12000
        Maximum total length of items in a batch for dynamic batching.
    mode : {'train', 'eval'}, default='train'
        If ``'train'`` the data will be shuffled before batching.

    Returns
    -------
    list of list
        A list of batches, where each batch is a list of data items.
    """
    if not isinstance(data, Sequence):
        raise TypeError("data must be a sequence (list, tuple, etc.)")

    # Optional shuffling
    if mode == 'train':
        data = list(data)
        random.shuffle(data)

    batches = []

    if batch_type == 'static':
        # Simple static batching
        for i in range(0, len(data), batch_size):
            batches.append(data[i:i + batch_size])

    elif batch_type == 'dynamic':
        # Dynamic batching based on total length
        current_batch = []
        current_frames = 0

        for item in data:
            item_len = _get_length(item)
            # If adding this item would exceed the limit, start a new batch
            if current_frames + item_len > max_frames_in_batch and current_batch:
                batches.append(current_batch)
                current_batch = []
                current_frames = 0

            current_batch.append(item)
            current_frames += item_len

        # Add the last batch if it has any items
        if current_batch:
            batches.append(current_batch)

    else:
        raise ValueError(f"Unknown batch_type: {batch_type!r}")

    return batches