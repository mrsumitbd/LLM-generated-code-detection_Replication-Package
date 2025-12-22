import torch

def create_optimizer(
    model: torch.nn.Module,
    learning_rate: float,
    betas: tuple[float, float],
    weight_decay: float,
) -> torch.optim.Optimizer:
    """
    Create an AdamW optimizer for the given model.

    Parameters
    ----------
    model : torch.nn.Module
        The model whose parameters will be optimized.
    learning_rate : float
        Learning rate for the optimizer.
    betas : tuple[float, float]
        Coefficients used for computing running averages of gradient and its square.
    weight_decay : float
        Weight decay (L2 penalty).

    Returns
    -------
    torch.optim.Optimizer
        The configured AdamW optimizer.
    """
    return torch.optim.AdamW(
        model.parameters(),
        lr=learning_rate,
        betas=betas,
        weight_decay=weight_decay,
    )