def to_cuda(batch):
    """Move batch data to CUDA device if available."""
    import torch
    
    if isinstance(batch, torch.Tensor):
        return batch.cuda() if torch.cuda.is_available() else batch
    elif isinstance(batch, dict):
        return {key: to_cuda(value) for key, value in batch.items()}
    elif isinstance(batch, (list, tuple)):
        return type(batch)(to_cuda(item) for item in batch)
    else:
        return batch