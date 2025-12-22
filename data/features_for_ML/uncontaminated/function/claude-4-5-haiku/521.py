def to_best_device(batch, device=get_best_device()):
    """Move batch to the best available device (GPU or CPU)."""
    if isinstance(batch, dict):
        return {key: to_best_device(value, device) for key, value in batch.items()}
    elif isinstance(batch, (list, tuple)):
        return type(batch)(to_best_device(item, device) for item in batch)
    elif hasattr(batch, 'to'):
        return batch.to(device)
    else:
        return batch