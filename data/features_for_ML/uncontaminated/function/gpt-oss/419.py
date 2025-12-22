import torch

def finalize_stat_tracker(
    tracker: dict[str, torch.Tensor], accelerator
) -> float | None:
    """
    Finalise a statistics tracker by aggregating metrics across all processes
    (if using distributed training) and returning the final loss value if
    present.

    Parameters
    ----------
    tracker : dict[str, torch.Tensor]
        Dictionary mapping metric names to tensors. Each tensor is expected
        to be a scalar (0‑d) tensor representing the metric value for the
        current process.
    accelerator : accelerate.Accelerator
        The accelerator instance used for distributed training. It is
        expected to provide a ``reduce`` method and a ``state`` attribute
        with ``num_processes`` (or ``world_size``) information.

    Returns
    -------
    float | None
        The aggregated loss value (as a Python float) if a key named
        ``"loss"`` exists in the tracker; otherwise ``None``.
    """
    if not tracker:
        return None

    # Determine the number of processes.  ``accelerator.state`` may expose
    # ``num_processes`` or ``world_size`` depending on the version.
    world_size = getattr(accelerator.state, "num_processes", None)
    if world_size is None:
        world_size = getattr(accelerator.state, "world_size", 1)

    # Aggregate each metric across processes.
    aggregated = {}
    for key, value in tracker.items():
        # Ensure we are working with a tensor.
        if not isinstance(value, torch.Tensor):
            raise TypeError(
                f"Tracker value for key '{key}' must be a torch.Tensor, "
                f"got {type(value).__name__}"
            )
        # Reduce (sum) the tensor across all processes.
        summed = accelerator.reduce(value, reduction="sum")
        # Compute the mean.
        mean = summed / world_size
        aggregated[key] = mean

    # Return the loss if it exists.
    loss_tensor = aggregated.get("loss")
    if loss_tensor is not None:
        # Detach and move to CPU before converting to Python float.
        return loss_tensor.detach().cpu().item()
    return None