import torch

def to_best_device(batch, device=get_best_device()):
    for key, value in batch.items():
        if isinstance(value, torch.Tensor):
            batch[key] = value.to(device)
    return batch