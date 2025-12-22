import torch

def update_param_fn(name: str, param: torch.Tensor) -> torch.Tensor:
            assert name == "density", "wrong paramaeter passed to update_param_fn"
            densities = torch.clamp(
                param,
                max=self.model.density_activation_inv(torch.tensor(self.new_max_density)).item(),
            )
            return torch.nn.Parameter(densities)