def finalize_stat_tracker(
    tracker: dict[str, torch.Tensor], accelerator
) -> float | None:
    """
    Finalize statistics from a tracker dictionary by gathering across all processes
    and computing the mean of the primary metric.
    """
    if not tracker:
        return None
    
    # Gather all tensors across processes
    for key in tracker:
        tracker[key] = accelerator.gather(tracker[key])
    
    # Compute mean for each metric
    for key in tracker:
        tracker[key] = tracker[key].mean().item()
    
    # Return the first metric value as the primary metric
    first_key = next(iter(tracker))
    return tracker[first_key]