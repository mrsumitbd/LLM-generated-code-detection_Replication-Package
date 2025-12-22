import torch
from torch.utils.data.dataloader import default_collate

def collate_fn(examples):
    """
    Collate a list of examples into a batch.

    Parameters
    ----------
    examples : list
        A list of examples returned by a Dataset. Each example can be a
        tensor, a numpy array, a scalar, a dict, a list, or a tuple.

    Returns
    -------
    batch : torch.Tensor or dict/list/tuple
        A batch of examples. For tensors, the batch will be a single
        tensor with an added batch dimension. For other types, the
        structure is preserved with each element collated into a
        list/tuple/dict of batched values.
    """
    return default_collate(examples)