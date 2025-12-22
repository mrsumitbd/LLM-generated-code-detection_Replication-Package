import torch

def add_fourier_features(inputs: torch.Tensor, start=6, stop=8, step=1):
    """
    Adds Fourier features to the input tensor.

    Args:
        inputs (torch.Tensor): The input tensor.
        start (int, optional): The starting frequency for the Fourier features. Defaults to 6.
        stop (int, optional): The ending frequency for the Fourier features. Defaults to 8.
        step (int, optional): The step size for the Fourier features. Defaults to 1.

    Returns:
        torch.Tensor: The input tensor with Fourier features added.
    """
    frequencies = torch.arange(start, stop, step)
    fourier_features = torch.cat([torch.sin(2 * torch.pi * inputs * freq) for freq in frequencies], dim=-1)
    return torch.cat([inputs, fourier_features], dim=-1)