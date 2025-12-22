import torch

def finalize_stat_tracker(tracker: dict[str, torch.Tensor], accelerator) -> float | None:
    if not tracker:
        return None

    total_sum = 0
    total_count = 0
    for key, value in tracker.items():
        total_sum += value.sum().item()
        total_count += value.numel()

    if total_count == 0:
        return None

    return total_sum / total_count