import torch
from typing import Tuple

class RectifiedFlowScaling:
    """
    A helper class for rectified flow scaling.

    Parameters
    ----------
    sigma_data : float, default 1.0
        The base sigma value used to compute the time variable.
    t_scaling_factor : float, default 1.0
        Scaling factor applied to the computed time variable.
    loss_weight_uniform : bool, default True
        If True, the loss weight is set to 1 for all sigma values.
        If False, the loss weight is computed as 1 / sigma^2.
    """

    def __init__(self, sigma_data: float = 1.0, t_scaling_factor: float = 1.0, loss_weight_uniform: bool = True):
        self.sigma_data = float(sigma_data)
        self.t_scaling_factor = float(t_scaling_factor)
        self.loss_weight_uniform = bool(loss_weight_uniform)

    def __call__(self, sigma: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Compute the rectified flow scaling components.

        Parameters
        ----------
        sigma : torch.Tensor
            Tensor of sigma values (must be positive).

        Returns
        -------
        Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]
            A tuple containing:
            - sigma (unchanged)
            - sigma_data tensor (broadcasted to match sigma shape)
            - t : time variable computed from sigma
            - loss_weight : weight for the loss term
        """
        if not torch.all(sigma > 0):
            raise ValueError("All sigma values must be positive.")

        # Broadcast sigma_data to the same shape as sigma
        sigma_data_tensor = torch.full_like(sigma, self.sigma_data)

        # Compute time variable t
        t = torch.log(sigma / sigma_data_tensor) * self.t_scaling_factor

        # Compute loss weight
        loss_weight = self.sigma_loss_weights(sigma)

        return sigma, sigma_data_tensor, t, loss_weight

    def sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
        """
        Compute loss weights based on sigma.

        Parameters
        ----------
        sigma : torch.Tensor
            Tensor of sigma values.

        Returns
        -------
        torch.Tensor
            Loss weight tensor of the same shape as sigma.
        """
        if self.loss_weight_uniform:
            return torch.ones_like(sigma)
        else:
            # Avoid division by zero
            eps = torch.finfo(sigma.dtype).eps
            return 1.0 / (sigma**2 + eps)