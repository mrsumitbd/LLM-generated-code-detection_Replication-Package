import torch

class RectifiedFlowScaling:
    def __init__(self, sigma_data: float = 1.0, t_scaling_factor: float = 1.0, loss_weight_uniform: bool = True):
        self.sigma_data = sigma_data
        self.t_scaling_factor = t_scaling_factor
        self.loss_weight_uniform = loss_weight_uniform

    def __call__(self, sigma: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        sigma_scaled = sigma * self.t_scaling_factor
        sigma_loss_weights = self.sigma_loss_weights(sigma_scaled)
        sigma_scaled_clipped = torch.clamp(sigma_scaled, min=self.sigma_data)
        sigma_scaled_rectified = torch.relu(sigma_scaled_clipped - self.sigma_data)
        return sigma_scaled, sigma_loss_weights, sigma_scaled_clipped, sigma_scaled_rectified

    def sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
        if self.loss_weight_uniform:
            return torch.ones_like(sigma)
        else:
            return 1.0 / (sigma + 1e-8)