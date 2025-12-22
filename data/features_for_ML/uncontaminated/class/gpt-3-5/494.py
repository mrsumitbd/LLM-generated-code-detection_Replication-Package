import torch

class RectifiedFlowScaling:

    def __init__(self, sigma_data: float = 1.0, t_scaling_factor: float = 1.0, loss_weight_uniform: bool = True):
        self.sigma_data = sigma_data
        self.t_scaling_factor = t_scaling_factor
        self.loss_weight_uniform = loss_weight_uniform

    def __call__(self, sigma: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        sigma_scaled = sigma * self.sigma_data
        t_scaled = sigma_scaled * self.t_scaling_factor
        sigma_weights = self.sigma_loss_weights(sigma)
        return sigma_scaled, t_scaled, sigma_weights, sigma_weights

    def sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
        if self.loss_weight_uniform:
            return torch.ones_like(sigma)
        else:
            return torch.abs(sigma)