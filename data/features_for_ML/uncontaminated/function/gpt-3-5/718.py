import torch

def create_optimizer(
    model: torch.nn.Module,
    learning_rate: float,
    betas: tuple[float, float],
    weight_decay: float,
) -> torch.optim.Optimizer:
    
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=learning_rate,
        betas=betas,
        weight_decay=weight_decay
    )
    
    return optimizer