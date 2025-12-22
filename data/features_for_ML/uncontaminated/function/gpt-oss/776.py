import torch
from typing import Tuple

def create_optimizer(
    model: "TrainableDecoder",
    learning_rate: float,
    betas: tuple[float, float],
    weight_decay: float,
) -> Tuple[torch.optim.Optimizer, torch.optim.Optimizer]:
    """
    Create optimizers for the generator and discriminator components of a GAN model.

    Parameters
    ----------
    model : TrainableDecoder
        The GAN model containing `generator` and `discriminator` attributes.
    learning_rate : float
        Learning rate for both optimizers.
    betas : tuple[float, float]
        Coefficients used for computing running averages of gradient and its square.
    weight_decay : float
        Weight decay (L2 penalty).

    Returns
    -------
    Tuple[torch.optim.Optimizer, torch.optim.Optimizer]
        Optimizer for the generator and optimizer for the discriminator.
    """
    # Determine the parameter groups for generator and discriminator.
    # If the model does not expose these attributes, fall back to the whole model.
    try:
        gen_params = model.generator.parameters()
    except AttributeError:
        gen_params = model.parameters()

    try:
        disc_params = model.discriminator.parameters()
    except AttributeError:
        disc_params = model.parameters()

    # Create Adam optimizers for each component.
    optimizer_g = torch.optim.Adam(
        gen_params,
        lr=learning_rate,
        betas=betas,
        weight_decay=weight_decay,
    )
    optimizer_d = torch.optim.Adam(
        disc_params,
        lr=learning_rate,
        betas=betas,
        weight_decay=weight_decay,
    )

    return optimizer_g, optimizer_d