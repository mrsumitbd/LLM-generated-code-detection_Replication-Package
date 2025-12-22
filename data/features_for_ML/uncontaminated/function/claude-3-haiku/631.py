def to_cuda(batch):
    if isinstance(batch, dict):
        for key, value in batch.items():
            batch[key] = value.cuda()
    elif isinstance(batch, list):
        batch = [item.cuda() for item in batch]
    elif isinstance(batch, torch.Tensor):
        batch = batch.cuda()
    else:
        raise TypeError("Unsupported batch type. Expected dict, list, or torch.Tensor.")
    return batch