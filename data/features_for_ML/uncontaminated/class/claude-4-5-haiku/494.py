import torch
import torch.nn as nn


class RectifiedFlowScaling:

    def __init__(self, sigma_data: float = 1.0, t_scaling_factor: float = 1.0, loss_weight_uniform: bool = True):
        self.sigma_data = sigma_data
        self.t_scaling_factor = t_scaling_factor
        self.loss_weight_uniform = loss_weight_uniform

    def __call__(self, sigma: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        sigma = sigma.to(torch.float32)
        
        # Compute scaling factors
        sigma_data = torch.tensor(self.sigma_data, dtype=torch.float32, device=sigma.device)
        
        # c_skip and c_out scaling
        c_skip = sigma_data ** 2 / (sigma ** 2 + sigma_data ** 2)
        c_out = sigma * sigma_data / torch.sqrt(sigma ** 2 + sigma_data ** 2)
        
        # c_in scaling
        c_in = 1 / torch.sqrt(sigma ** 2 + sigma_data ** 2)
        
        # c_noise scaling with t_scaling_factor
        c_noise = sigma.log() / 4
        c_noise = c_noise * self.t_scaling_factor
        
        return c_skip, c_out, c_in, c_noise

    def sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
        sigma = sigma.to(torch.float32)
        sigma_data = torch.tensor(self.sigma_data, dtype=torch.float32, device=sigma.device)
        
        if self.loss_weight_uniform:
            # Uniform weighting
            return torch.ones_like(sigma)
        else:
            # Weighting based on sigma
            # Weight inversely proportional to (sigma^2 + sigma_data^2)
            weights = 1 / (sigma ** 2 + sigma_data ** 2)
            return weights