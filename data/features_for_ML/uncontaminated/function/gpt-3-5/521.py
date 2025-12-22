def to_best_device(batch, device=get_best_device()):
    return batch.to(device)