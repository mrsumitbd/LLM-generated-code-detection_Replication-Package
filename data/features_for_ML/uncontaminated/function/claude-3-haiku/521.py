def to_best_device(batch, device=get_best_device()):
    """
    Moves the given batch of data to the specified device.

    Args:
        batch (torch.Tensor or list of torch.Tensor): The batch of data to be moved to the device.
        device (torch.device, optional): The device to move the batch to. If not specified, the best available device will be used.

    Returns:
        torch.Tensor or list of torch.Tensor: The batch of data moved to the specified device.
    """
    if isinstance(batch, (list, tuple)):
        return [item.to(device) for item in batch]
    else:
        return batch.to(device)