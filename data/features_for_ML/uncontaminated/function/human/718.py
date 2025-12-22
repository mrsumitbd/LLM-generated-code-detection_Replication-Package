import torch

def create_optimizer(
    model: torch.nn.Module,
    learning_rate: float,
    betas: tuple[float, float],
    weight_decay: float,
) -> torch.optim.Optimizer:
    return torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate,
        betas=betas,
        weight_decay=weight_decay,
        fused=True,
    )