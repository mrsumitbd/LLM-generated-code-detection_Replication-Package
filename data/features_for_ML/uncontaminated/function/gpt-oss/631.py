import torch

def to_cuda(batch):
    """
    Recursively move a batch of data to CUDA.
    Supports dicts, lists, tuples, and torch Tensors.
    """
    if isinstance(batch, torch.Tensor):
        return batch.cuda()
    elif isinstance(batch, dict):
        return {k: to_cuda(v) for k, v in batch.items()}
    elif isinstance(batch, (list, tuple)):
        return type(batch)(to_cuda(v) for v in batch)
    else:
        return batch