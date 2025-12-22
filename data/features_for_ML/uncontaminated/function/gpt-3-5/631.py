def to_cuda(batch):
    import torch
    if isinstance(batch, torch.Tensor):
        return batch.cuda()
    elif isinstance(batch, (list, tuple)):
        return [to_cuda(item) for item in batch]
    elif isinstance(batch, dict):
        return {key: to_cuda(value) for key, value in batch.items()}
    else:
        return batch