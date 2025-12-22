import torch

def finalize_stat_tracker(
    tracker: dict[str, torch.Tensor], accelerator
) -> float | None:
    try:
        for key, value in tracker.items():
            tracker[key] = value.to(accelerator.device)
        loss = tracker["loss"].mean()
        return loss.item()
    except (KeyError, AttributeError):
        return None