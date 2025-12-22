import torch

def finalize_stat_tracker(
    tracker: dict[str, torch.Tensor], accelerator
) -> float | None:
    total_count = accelerator.gather(tracker["count"]).sum()
    if total_count.item() == 0:
        return None

    total_sum = accelerator.gather(tracker["sum"]).sum()
    mean = (total_sum / total_count).float().item()

    return mean